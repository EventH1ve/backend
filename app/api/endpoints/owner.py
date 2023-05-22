from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from models.user import User as ModelUser
from models.admin import Admin as ModelAdmin
from models.event import Event as ModelEvent, UserEventBooking as ModelUserEventBooking
from schemas.owner import OwnerMetrics
from fastapi_sqlalchemy import db
from sqlalchemy import func


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