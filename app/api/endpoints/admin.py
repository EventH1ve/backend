from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_sqlalchemy import db
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent, UserEventBooking
from models.ticket import TicketType as ModelTicketType
from models.admin import Admin as ModelAdmin
from models.user import User as ModelUser
from schemas.event import SingleEvent, AdminEvent as ModelAdminEvent
from datetime import datetime


router = APIRouter()


@router.get('/event/{id}', response_model=SingleEvent)
async def getAdminEvent(id: int, userId: Annotated[int, Depends(getCurrentUserId)]):
    event = db.session.query(ModelEvent).with_entities(
        ModelEvent.id,
        ModelEvent.name,
        ModelEvent.venue,
        ModelEvent.description,
        ModelEvent.eventstartdatetime.label("date"),
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


@router.get('/event/statistics/{id}')
async def getEventStatistics(id: int, userId: Annotated[int, Depends(getCurrentUserId)]):

    # Get admin id
    adminId = db.session.query(ModelAdmin).with_entities(ModelAdmin.id).filter(ModelAdmin.userid == userId).first()[0]

    if not adminId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not an Admin.')

    #Get event to fetch event details
    event = db.session.query(ModelEvent).filter(ModelEvent.adminid == adminId, ModelEvent.id == id).first()
    # event = event.dict()
    
    if not event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Event not found.')

    #Fetch the user that serves as event admin for his details
    eventAdmin = db.session.query(ModelUser).filter(ModelUser.id == userId).first()
    # eventAdmin = eventAdmin.dict()
    
    #Fetch all purchased tickets of this event
    eventTickets = db.session.query(UserEventBooking).filter(UserEventBooking.eventid == id).all() 
    # eventTickets = eventTickets.dict()
    
    #Fetch all ticket types of this event
    eventTicketTypes = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == id).all()
    # eventTicketTypes = eventTicketTypes.dict()

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

    # Initialize genderPercentage
    genderPercentage['Total'] = [0] * 2
    for ticketType in eventTicketTypes:
        genderPercentage[ticketType.name] = [0] * 2
    
    #Event tickets analytics
    ticketsData = dict(list())
    '''TicketsData = {
        "Total" = [total checked in tickets => checked, total event capacity from all ticketTypes => event.capacity]
        "ticketType1": [number of checked tickets of this type, total number of tickets available of this type => ticketType.limit]
        "ticketType2": [10, 20],
        "ticketType3": [20, 40],
        ...
    }'''

    # Initialize ticketsData
    ticketsData['Total'] = [0] * 2
    for ticketType in eventTicketTypes:
        ticketsData[ticketType.name] = [0] * 2

    #Store all event attendees
    eventAttendees = []

    #For each bought ticket
    for ticket in eventTickets:
        ticketType = db.session.query(ModelTicketType).filter(ModelTicketType.eventid == id, ModelTicketType.name == ticket.tickettype).first()
        #Add the ticket price to the total revenue
        revenue+= ticket.price

        if(ticket.checkedin):
            #If the ticket is checked, add it to the checked tickets count and  
            checked += 1
            #Add the ticket as a checked ticket for this specific ticket type
            ticketsData[ticket.tickettype][0] += 1

        #Get the attendee who bought this ticket
        attendee = db.session.query(ModelUser).filter(ModelUser.id == ticket.userid).first()
        
        #Append this user as event attendee
        eventAttendees.append(attendee)

        #Increment gender percentage for either male or female count for this specific ticket type
        if(attendee.gender.lower() == 'male'):
            genderPercentage[ticket.tickettype][0] += 1
            genderPercentage['Total'][0] += 1
        else:
            genderPercentage[ticket.tickettype][1] += 1
            genderPercentage['Total'][1] += 1
        
        #For each ticket Type, Set the total available tickets of this type => ticketType.limit and add it to ticketsData
        ticketsData[ticket.tickettype][1] = ticketType.limit

    #Set total ticketsData => [total checked tickets, total event capacity]
    ticketsData['Total'] = [checked, event.capacity]

    eventStatistics = {
        "name": event.name,
        "cover": event.profile,
        "date": event.eventstartdatetime.date(),
        "time": event.eventstartdatetime.time(),
        "description": event.description,
        "venue": event.venue,
        "organizer": eventAdmin.username,
        "counters": {
            "capacity": event.capacity,
            "soldTickets": len(eventTickets),
            "revenue": revenue,
            "checkedIn": checked,
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

    existing_event = db.session.query(ModelEvent).filter(ModelEvent.id == event_id).first()
    if not existing_event:
        return {
            "success": False,
            "message": "Event not found."
        }
    
    event_data = event.dict(exclude={"ticketTypes"})

    admin = db.session.query(ModelAdmin).filter(ModelAdmin.userid == userId).first()
    if not admin:
        return {
            "success": False,
            "message": "Admin who created the event not found."
        }

    event_datetime_str = "T".join([event.date, event.time])
    event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%dT%H:%M:%S")
    event_data["datetime"] = event_datetime
    
    event_data.pop("date", None)
    event_data.pop("time", None)

    #Existing_event.update(event_data)
    existing_event.name        = event_data['name']        
    existing_event.profile     = event_data['profile'] 
    existing_event.description = event_data['description'] 
    existing_event.venue       = event_data['venue']   
    existing_event.datetime    = event_data['datetime'] 

    db.session.commit()

    # Update exsiting ticket types or create new ticket types
    for ticket_type in event.ticketTypes:

        ticket_type_data = ticket_type.dict()

        existing_ticket_type = (
            db.session.query(ModelTicketType)
            .filter(ModelTicketType.eventid == event_id, ModelTicketType.name == ticket_type.name)
            .first()
        )
        #Existing_ticket_type.update(ticket_type_data)
        if existing_ticket_type:
            existing_ticket_type.name = ticket_type.name
            existing_ticket_type.price = ticket_type.price
            existing_ticket_type.limit = ticket_type.limit
            existing_ticket_type.seated = ticket_type.seated
            existing_ticket_type.seats = ticket_type.seats
        else:
            ticket_type_data["eventid"] = event_id
            createdTicketType = ModelTicketType(**ticket_type_data)
            db.session.add(createdTicketType)

    db.session.commit()

    return {
        "success": True,
        "message": "Event updated."
    }
