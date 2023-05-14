from datetime import datetime
from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import func
from models.event import Event as ModelEvent
from models.ticket import TicketType as ModelTicketType
from schemas.event import MobileEvent


router = APIRouter()

@router.get('/{id}', response_model=List[MobileEvent])
async def findEventByAdmin(id: int,skip: int = 0, limit: int = 10):
    events = []
    now = datetime.now().date()
    for event in db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.description,
        ModelEvent.adminid,
        ModelEvent.venue,
        ModelEvent.eventstartdatetime.label("date"),
        func.min(ModelTicketType.price).label("price"),
        ModelEvent.profile,
    ).filter(ModelEvent.adminid == id).join(ModelTicketType, isouter=True).group_by(ModelEvent.id).offset(skip).limit(limit).all():
        eventstartdatetime = event.date
        isEnabled = True if eventstartdatetime.date() == now else False
        types = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == event.id).all()

        eventDict = {
            "id":event.id,
            "name": event.name,
            "venue": event.venue,
            "date": event.date,
            "price": event.price,
            "profile": event.profile,
            "isEnabled": isEnabled,
            "tickettypes": types

            
        }
        singleEvent = MobileEvent.parse_obj(eventDict)
        events.append(singleEvent)
    return events
