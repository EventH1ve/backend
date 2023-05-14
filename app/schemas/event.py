from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from schemas.ticket import TicketType

class Event(BaseModel):
    id: Optional[int] = None
    name: str
    coverImage: str
    datetime: datetime
    description: str
    venue: str

    creationdate: Optional[datetime]
    type: Optional[str]
    status: Optional[str]
    registrationstartdatetime: Optional[datetime]
    registrationenddatetime: Optional[datetime]
    eventstartdatetime: Optional[datetime]
    eventenddatetime: Optional[datetime]


    class Config:
        orm_mode = True


class UserEventBooking(BaseModel):
    id: Optional[int] = None
    userid: int
    eventid: int
    bookingdate: datetime
    price: float
    transactionid: str

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


class SingleEvent(BaseModel):
    name: str
    venue: str
    date: datetime
    profile: str
    tickettypes: List[TicketType]

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
