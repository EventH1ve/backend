from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from models.user import User as ModelUser
from models.admin import Admin as ModelAdmin
from models.event import Event as ModelEvent, UserEventBooking as ModelUserEventBooking
from schemas.owner import OwnerMetrics, OrganizerRequest, UnapprovedAdmin
from fastapi_sqlalchemy import db
from sqlalchemy import func
import bcrypt


router = APIRouter()


@router.get('/',response_model=OwnerMetrics)
async def getOwnerMetrics():
    organizers = (db.session.query(func.count(ModelUser.id))
                  .filter(ModelUser.type == 'admin')
                  .scalar())
    
    attendees = (db.session.query(func.count(ModelUser.id))
                  .filter(ModelUser.type == 'user')
                  .scalar())
    
    activeEvents = (db.session.query(func.count(ModelEvent.id))
                    .filter(ModelEvent.eventstartdatetime > datetime.isoformat(datetime.now()))
                    .scalar())
    
    transactionsProcessed = (db.session.query(func.count(ModelUserEventBooking.id))
                             .scalar())

    admins = (db.session.query(ModelUser)
              .with_entities(
                ModelUser.id,
                (ModelUser.firstname + ' ' + ModelUser.lastname).label('name'),
                ModelUser.email,
                ModelUser.phonenumber,
                (ModelAdmin.membershipend - datetime.now()).label('remainingQuantity')
            ).join(ModelAdmin).all())
    
    adminList = list()

    for admin in admins:
        adminList.append({
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
            "phonenumber": admin.phonenumber,
            "remainingQuantity": admin.remainingQuantity.days
        })

    return {
        "counters":{
            "organizers": organizers,
            "attendees": attendees,
            "totalAccounts": (organizers + attendees),
            "activeEvents": activeEvents,
            "transactionsProcessed": transactionsProcessed
        },
        "admins": adminList
    }


@router.post('/request')
async def organizerRequest(orgReq: OrganizerRequest):
    query = db.session.query(ModelUser).filter(ModelUser.username == orgReq.username).first()
   
    if query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists.')

    orgReq.password = bcrypt.hashpw(orgReq.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    userModel = ModelUser()

    userModel.username = orgReq.username
    userModel.email = orgReq.email
    userModel.password = orgReq.password
    userModel.gender = orgReq.gender
    userModel.phonenumber = orgReq.phonenumber
    userModel.firstname = orgReq.firstname
    userModel.lastname = orgReq.lastname
    userModel.type = "admin"

    db.session.add(userModel)
    db.session.commit()
    
    adminModel = ModelAdmin(userid=userModel.id)
    adminModel.logo = orgReq.logo
    db.session.add(adminModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Request placed."
    }


@router.get('/unapproved', response_model=List[UnapprovedAdmin])
async def getUnapproveedAdmins():
    admins = (db.session.query(ModelAdmin)
              .filter(ModelAdmin.active.is_(False))
              .all())
    
    users = list()

    for admin in admins:
        users.append({
            "id": admin.user.id,
            "username": admin.user.username,
            "firstname": admin.user.firstname,
            "lastname": admin.user.lastname,
            "email": admin.user.email,
        })
    
    return users
    
