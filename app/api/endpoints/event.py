from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import func
from models.event import Event as ModelEvent
from models.venue import Venue as ModelVenue
from models.ticket import TicketType as ModelTicketType
from schemas.event import Event, ClientEvent


router = APIRouter()


@router.get('/', response_model=List[ClientEvent])
async def listEvents(skip: int = 0, limit: int = 10):
    events = db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelVenue.name.label("venue"),
        ModelEvent.eventstartdatetime.label("date"),
        func.min(ModelTicketType.price).label("price"),
        ModelEvent.profile,
    ).join(ModelVenue).join(ModelTicketType).group_by(ModelEvent.id, ModelVenue.name).all()
    return events


@router.post('/')
async def createEvent(event: Event):
    eventModel = ModelEvent(**event.dict())

    db.session.add(eventModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Event created."
    }
