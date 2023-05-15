from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent, UserEventBooking
from models.ticket import TicketType as ModelTicketType, Ticket as ModelTicket
from models.admin import Admin as ModelAdmin
from models.user import User as ModelUser
from schemas.event import Event, ListEvent, SingleEvent

router = APIRouter()

@router.post('/event')
async def createEvent(event: Event, userId: Annotated[int, Depends(getCurrentUserId)]):

    event_data = event.dict(exclude={"ticketTypes"})
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


@router.get('/event', response_model=List[ListEvent])
async def getAdminEvents(userId: Annotated[int, Depends(getCurrentUserId)], skip: int = 0, limit: int = 10):
    events = db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.venue,
        ModelEvent.datetime.label("date"),
        ModelEvent.profile,
    ).filter(ModelEvent.adminid == userId).group_by(ModelEvent.id).offset(skip).limit(limit).all()
        
    return events

@router.get('/event/{id}', response_model=SingleEvent)
async def getAdminEvent(id: int, userId: Annotated[int, Depends(getCurrentUserId)]):
    event = db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.venue,
        ModelEvent.description,
        ModelEvent.datetime.label("date"),
        ModelEvent.profile,
    ).filter(ModelEvent.adminid == userId, ModelEvent.id == id).first()     #[0]

    ticketTypes = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == event.id).all()
    eventBookingCount = len( db.session.query(UserEventBooking).filter(UserEventBooking.eventid == event.id).all() )

    eventDict = {
        "name": event.name,
        "venue": event.venue,
        "date": event.date,
        "description": event.description,
        "cover": event.profile,
        "attendess": eventBookingCount,
        "tickettypes": ticketTypes
    }
        
    return eventDict

# @router.get('/event/{id}')
# async def updateEvent(userId: Annotated[int, Depends(getCurrentUserId)], newEvent: ModelEvent):
#     oldEvent = db.session.query(ModelEvent).filter(ModelEvent.admin_id == userId, ModelEvent.id == id).first()[0]
#     # update event

@router.get('event/statistics/{id}')
async def getEventStatistics(userId: Annotated[int, Depends(getCurrentUserId)]):

    event = db.session.query(ModelEvent).filter(ModelEvent.adminid == userId, ModelEvent.id == id).first()
    eventAdmin = db.session.query(ModelUser).filter(ModelUser.id == userId).first()
    eventTickets = db.session.query(UserEventBooking).filter(UserEventBooking.eventid == id).all() #all bought and created tickets
    eventTicketTypes = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == id).all()

    checked = 0
    revenue = 0
    genderPercentage = dict(list())
    ticketsData = dict(list())
    
    for ticket in eventTickets:
        revenue+= ticket.price
        if(ticket.checked):
            checked+=1
            ticketsData[ticket.type][0]+=1
        user = db.session.query(ModelUser).filter(ModelUser.id == ticket.userid)
        if(user.gender.toLowwer() == 'male'):
            genderPercentage[ticket.type][0]+=1
        else:
            genderPercentage[ticket.type][1]+=1

        genderPercentage[ticket.type].totalCount+=1

    for ticketType in eventTicketTypes:
        ticketsData[ticketType][1] = ticketType.limit

    ticketsData['Total'] = [checked, event.capacity]

    eventAttendees = []
    for ticket in eventTickets:
        attendee = db.session.query(ModelUser).filter(ModelUser.id == ticket.userid).all()
        eventAttendees.append(attendee)

    eventid_statistics = {
        "name": event.name,
        "cover": event.profile,
        "date": event.datetime,
        "description": event.description,
        "time": event.time,
        "venue": event.venue,
        "organizer": eventAdmin.username,
        "counters": {
            "capacity": event.capacity,
            "soldTickets": len(eventTickets),
            "revenue": revenue,
            "checked": checked,
            "gateStaff": 5,
        },
        "genderPercentage":  genderPercentage,
        "ticketsData": ticketsData,
        "ticketTypes": eventTicketTypes,
        "attendess": eventAttendees
    }
