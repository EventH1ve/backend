from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_sqlalchemy import db
from schemas.ticket import TicketType, TicketValidity, TicketInfo
from schemas.event import UserEventBooking
from models.ticket import TicketType as ModelTicketType
from models.user import User as ModelUser
from models.event import UserEventBooking as ModelUserEventBooking
from lib.auth.jwt_bearer import getCurrentUserId

router = APIRouter()


@router.post('/verify', response_model=TicketValidity)
async def verifyTicketValidity(userId: Annotated[int, Depends(getCurrentUserId)], ticketInfo: TicketInfo):
    userType = (db.session.query(ModelUser)
            .with_entities(ModelUser.type)
            .filter(ModelUser.id == userId).first())
    
    if userType[0].lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not an Admin.')

    booking = (db.session.query(ModelUserEventBooking)
               .filter(ModelUserEventBooking.id == ticketInfo.ticketId).first())
    
    booking.checkedin = True
    db.session.commit()

    userBooking = UserEventBooking.from_orm(booking)

    return TicketValidity(valid=((ticketInfo.gate.lower() == userBooking.tickettype.lower()) and (ticketInfo.eventId == userBooking.eventid)))



@router.post('/type')
async def createTicketType(ticketType: TicketType):
    ticketTypeModel = ModelTicketType(**ticketType.dict())

    db.session.add(ticketTypeModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Ticket type created."
    }


@router.get('/type', response_model=List[TicketType])
async def listTicketTypes():
    ticketTypes = db.session.query(ModelTicketType).all()
    return ticketTypes