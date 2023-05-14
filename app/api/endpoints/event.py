from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy import func
from models.user import User as ModelUser
from models.event import Event as ModelEvent
from models.ticket import TicketType as ModelTicketType
from schemas.event import Event, ListEvent, SingleEvent
from lib.auth.jwt_bearer import getCurrentUserId


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
        ModelEvent.description,
        ModelEvent.venue,
        ModelEvent.eventstartdatetime.label("date"),
        ModelEvent.profile,
    ).filter(ModelEvent.id == id).all():
        types = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == event.id).all()
        eventDict = {
            "name": event.name,
            "description":event.description,
            "venue": event.venue,
            "date": event.date,
            "cover": event.profile,
            "tickettypes": types
        }
        singleEvent = SingleEvent.parse_obj(eventDict)
        events.append(singleEvent)
    return events


@router.post('/')
async def createEvent(event: Event, userId: Annotated[int, Depends(getCurrentUserId)]):
    userType = (db.session.query(ModelUser)
            .with_entities(ModelUser.type)
            .filter(ModelUser.id == userId).first())
    
    if userType[0].lower() != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not an Admin.')

    event.adminid = userId

    eventModel = ModelEvent(**event.dict())

    db.session.add(eventModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Event created."
    }
