from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy import func
from models.user import User as ModelUser
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent
from models.ticket import TicketType as ModelTicketType
from schemas.event import Event, ListEvent, SingleEvent, MobileEvent, AdminEvent
from lib.auth.jwt_bearer import getCurrentUserId
from models.admin import Admin as ModelAdmin


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


@router.get('/app', response_model=List[MobileEvent])
async def findEventsByAdmin(userId: Annotated[int, Depends(getCurrentUserId)], skip: int = 0, limit: int = 10):
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
    ).filter(ModelEvent.adminid == userId).join(ModelTicketType, isouter=True).group_by(ModelEvent.id).offset(skip).limit(limit).all():
        eventstartdatetime = event.date
        isEnabled = True if eventstartdatetime.date() == now else False
        types = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == event.id).all()

        eventDict = {
            "id": event.id,
            "name": event.name,
            "venue": event.venue,
            "date": event.date,
            "price": event.price,
            "img": event.profile,
            "isEnabled": isEnabled,
            "tickettypes": types
        }

        singleEvent = MobileEvent.parse_obj(eventDict)
        events.append(singleEvent)

    return events


@router.get('/{id}', response_model=SingleEvent)
async def findEventById(id: int):
    event = db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.description,
        ModelEvent.venue,
        ModelEvent.eventstartdatetime.label("date"),
        ModelEvent.profile,
    ).filter(ModelEvent.id == id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Event not found.')

    types = (db.session.query(ModelTicketType)
                .filter(ModelTicketType.eventid == event.id).all())
    eventDict = {
        "name": event.name,
        "description":event.description,
        "venue": event.venue,
        "date": event.date,
        "cover": event.profile,
        "tickets": types
    }
    singleEvent = SingleEvent.parse_obj(eventDict)
    return singleEvent


@router.post('/')
async def createEvent(event: AdminEvent, userId: Annotated[int, Depends(getCurrentUserId)]):
    event_data = event.dict(exclude={"ticketTypes"})
    event_datetime_str = "T".join([event.date, event.time])
    event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%dT%H:%M:%S")
    event_data["eventstartdatetime"] = event_datetime
    
    event_data.pop("date", None)
    event_data.pop("time", None)
    admin = db.session.query(ModelAdmin).filter(ModelAdmin.userid == userId).first()
    if not admin:
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
