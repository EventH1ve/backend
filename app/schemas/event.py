from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from schemas.ticket import TicketType
from uuid import UUID

class Event(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    venue: str
    type: str
    status: str
    creationdate: Optional[datetime]
    registrationstartdatetime: datetime
    registrationenddatetime: datetime
    eventstartdatetime: datetime
    eventenddatetime: datetime
    profile: str
    adminid: Optional[int]

    class Config:
        orm_mode = True


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


class EventSeatLayout(BaseModel):
    id: Optional[int] = None
    eventid: int
    row: str
    seats: List[int]


class ReceivedEvent(BaseModel):
    name: str
    cover: str
    date: str
    description: str
    time: str
    venue: str
    tickets: List[dict]