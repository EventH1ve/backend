from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent
from models.ticket import TicketType as ModelTicketType
from schemas.event import Event, ListEvent, SingleEvent

router = APIRouter()

@router.post('/')
async def createEvent(event: Event, userId: Annotated[int, Depends(getCurrentUserId)]):

    event_data = event.dict(exclude={"ticketTypes"})
    event_data['admin_id'] = userId
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

