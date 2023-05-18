from typing import Optional, List
from datetime import datetime, date, time
from pydantic import BaseModel
from schemas.ticket import TicketType, AdminTicketType
from uuid import UUID

class Event(BaseModel):
    id: Optional[int] = None
    name: str
    profile: str
    capacity: int
    datetime: datetime
    description: str
    venue: str
    ticketTypes: List[TicketType]
    creationdate: Optional[datetime]
    adminid: Optional[int]
    type: Optional[str]
    status: Optional[str]
    registrationstartdatetime: Optional[datetime]
    registrationenddatetime: Optional[datetime]
    eventstartdatetime: Optional[datetime]
    eventenddatetime: Optional[datetime]

    class Config:
        orm_mode = True


class AdminEvent(BaseModel):
    name: str
    profile: str
    capacity: int
    date: str
    time: str
    description: str
    venue: str
    ticketTypes: List[AdminTicketType]


class UserEventBooking(BaseModel):
    id: Optional[UUID] = None
    userid: int
    eventid: int
    bookingdate: datetime
    price: float
    transactionid: str
    tickettype: str
    checkedin: Optional[bool] = False 

    class Config:
        orm_mode = True


class ListEvent(BaseModel):
    id: int
    name: str
    venue: str
    date: datetime
    price: Optional[int] = 0
    profile: str

    class Config:
        orm_mode = True


class MobileEvent(BaseModel):
    id: int
    name: str
    venue: str
    date: datetime
    price: Optional[int] = 0
    img: str
    isEnabled:str
    tickettypes: List[TicketType]

    class Config:
        orm_mode = True

    
class SingleEvent(BaseModel):
    name: str
    venue: str
    date: datetime
    cover: str  # change "profile" to "cover"
    tickets: List[TicketType]
    description:str


    class Config:
        orm_mode = True


class DashboardEvent(BaseModel):
    id: Optional[int] = None
    name: str
    venue: str
    date: datetime
    price: float
    status: Optional[str] = "Paid"
    transactionid: str

    class Config:
        orm_mode = True

class DashboardEventAdmin(BaseModel):
    id: Optional[int] = None
    name: str
    venue: str
    date: datetime
        
    class Config:
        orm_mode = True



class ReceivedEvent(BaseModel):
    name: str
    cover: str
    date: str
    description: str
    time: str
    venue: str
    tickets: List[dict]