from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent, UserEventBooking
from models.ticket import TicketType as ModelTicketType, Ticket as ModelTicket
from models.admin import Admin as ModelAdmin
from models.user import User as ModelUser
from schemas.event import Event, ListEvent, SingleEvent, AdminEvent as ModelAdminEvent

router = APIRouter()

@router.post('/event')
async def createEvent(event: ModelAdminEvent, userId: Annotated[int, Depends(getCurrentUserId)]):

    event_data = event.dict(exclude={"ticketTypes"})

    admin = db.session.query(ModelAdmin).filter(ModelAdmin.userid == userId).first()
    if(not admin):
        adminModel = ModelAdmin(userid=userId)
        db.session.add(adminModel)
        db.session.commit()
    
    event_data['adminid'] = userId
    createdEvent = ModelEvent(**event_data)
    db.session.add(createdEvent)
    db.session.commit()


    for ticket_type in event.ticketTypes:
        ticket_type_data = ticket_type.dict()
        ticket_type_data["eventid"] = createdEvent.id  
        createdTicketType = ModelTicketType(**ticket_type_data)
        db.session.add(createdTicketType)

    db.session.commit()

    return {
        "success": True,
        "message": "Event created."
    }

