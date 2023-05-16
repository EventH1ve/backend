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
    ).filter(ModelEvent.adminid == userId, ModelEvent.id == id).first()     

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

@router.get('event/statistics/{id}')
async def getEventStatistics(id: int,userId: Annotated[int, Depends(getCurrentUserId)]):

    #Get event to fetch event details
    event = db.session.query(ModelEvent).filter(ModelEvent.adminid == userId, ModelEvent.id == id).first()
    #Fetch the user that serves as event admin for his details
    eventAdmin = db.session.query(ModelUser).filter(ModelUser.id == userId).first()
    #Fetch all purchased tickets of this event
    eventTickets = db.session.query(UserEventBooking).filter(UserEventBooking.eventid == id).all() 
    #Fetch all ticket types of this event
    eventTicketTypes = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == id).all()

    #Number of checked tickets
    checked = 0
    #Total revenue of the event tickets
    revenue = 0
    
    #Event gender percentage
    genderPercentage = dict(list())
    '''genderPercentage = {
        "ticketType1": [number of tickets of male attendees, number of tickets of female attendees]
        "ticketType2": [10, 20],
        "ticketType3": [20,15],
        ...
    }'''

    
    #Event tickets analytics
    ticketsData = dict(list())
    '''TicketsData = {
        "Total" = [total checked in tickets => checked, total event capacity from all ticketTypes => event.capacity]
        "ticketType1": [number of checked tickets of this type, total number of tickets available of this type => ticketType.limit]
        "ticketType2": [10, 20],
        "ticketType3": [20, 40],
        ...
    }'''

    #Store all event attendees
    eventAttendees = []

    #For each bought ticket
    for ticket in eventTickets:
        #Add the ticket price to the total revenue
        revenue+= ticket.price

        if(ticket.checked):
            #If the ticket is checked, add it to the checked tickets count and  
            checked+=1
            #Add the ticket as a checked ticket for this specific ticket type
            ticketsData[ticket.type][0]+=1

        #Get the attendee who bought this ticket
        attendee = db.session.query(ModelUser).filter(ModelUser.id == ticket.userid).first()
        
        #Append this user as event attendee
        eventAttendees.append(attendee)

        #Increment gender percentage for either male or female count for this specific ticket type
        if(attendee.gender.lower() == 'male'):
            genderPercentage[ticket.type][0]+=1
        else:
            genderPercentage[ticket.type][1]+=1

        #Total attendees of this ticket type
        genderPercentage[ticket.type].totalCount+=1

    #For each ticket Type, Set the total available tickets of this type => ticketType.limit and add it to ticketsData
    for ticketType in eventTicketTypes:
        ticketsData[ticketType][1] = ticketType.limit

    #Set total ticketsData => [total checked tickets, total event capacity]
    ticketsData['Total'] = [checked, event.capacity]

    eventStatistics = {
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

    return eventStatistics

@router.put('/event/{event_id}')
async def updateEvent(event_id: int, event: ModelAdminEvent, userId: Annotated[int, Depends(getCurrentUserId)]):

    event_data = event.dict(exclude={"ticketTypes"})

    admin = db.session.query(ModelAdmin).filter(ModelAdmin.userid == userId).first()
    if not admin:
        adminModel = ModelAdmin(userid=userId)
        db.session.add(adminModel)
        db.session.commit()

    event_data['adminid'] = userId

    existing_event = db.session.query(ModelEvent).filter(ModelEvent.id == event_id).first()
    if not existing_event:
        return {
            "success": False,
            "message": "Event not found."
        }

    existing_event.update(event_data)
    db.session.commit()

    # Update exsiting ticket types or create new ticket types
    for ticket_type in event.ticketTypes:

        ticket_type_data = ticket_type.dict()
        ticket_type_data["eventid"] = event_id

        existing_ticket_type = (
            db.session.query(ModelTicketType)
            .filter(ModelTicketType.eventid == event_id, ModelTicketType.name == ticket_type.name)
            .first()
        )
        if existing_ticket_type:
            existing_ticket_type.update(ticket_type_data)
        else:
            createdTicketType = ModelTicketType(**ticket_type_data)
            db.session.add(createdTicketType)

    db.session.commit()

    return {
        "success": True,
        "message": "Event updated."
    }
