from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from schemas.ticket import TicketType

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

    class Config:
        orm_mode = True


class UserEventBooking(BaseModel):
    id: Optional[int] = None
    userid: int
    eventid: int
    bookingdate: datetime
    price: float
    transactionid: str


class ListEvent(BaseModel):
    id: int
    name: str
    venue: str
    date: str
    price: str
    profile: str

    class Config:
        orm_mode = True


class SingleEvent(BaseModel):
    name: str
    venue: str
    date: str
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
    transactionId: str