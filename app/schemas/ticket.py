from typing import Dict, List, Optional
from pydantic import BaseModel


class Ticket(BaseModel):
    id: int
    type: int
    eventid: int
    qrcode: str
    seatnumber: int

    class Config:
        orm_mode = True


class TicketType(BaseModel):
    id: Optional[int] = None
    eventid: int
    name: str
    price: int
    limit: int
    seated: bool
    seats: Dict[str, List[int]]


    class Config:
        orm_mode = True


class ReceievedTicketType(BaseModel):
    name: str
    price: float
    available: bool
    seated: bool


class TicketValidity(BaseModel):
    valid: bool


class TicketInfo(BaseModel):
    ticketId: str
    gate: str
    eventId: int