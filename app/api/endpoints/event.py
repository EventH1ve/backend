from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent
from models.ticket import TicketType as ModelTicketType
from schemas.event import Event, ListEvent, SingleEvent


router = APIRouter()


@router.get('/', response_model=List[ListEvent])
async def listEvents(skip: int = 0, limit: int = 10):
    events = db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.venue,
        ModelEvent.eventstartdatetime.label("date"),
        func.min(ModelTicketType.price).label("price"),
        ModelEvent.profile,
    ).join(ModelTicketType, isouter=True).group_by(ModelEvent.id).offset(skip).limit(limit).all()
    return events


@router.get('/{id}', response_model=List[SingleEvent])
async def findEvent(id: int):
    events = []
    for event in db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.venue,
        ModelEvent.eventstartdatetime.label("date"),
        ModelEvent.profile,
    ).filter(ModelEvent.id == id).all():
        types = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == event.id).all()
        eventDict = {
            "name": event.name,
            "venue": event.venue,
            "date": event.date,
            "profile": event.profile,
            "tickettypes": types
        }
        singleEvent = SingleEvent.parse_obj(eventDict)
        events.append(singleEvent)
    return events
