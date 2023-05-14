from typing import Optional
from pydantic import BaseModel, Json


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
    seats: Json


    class Config:
        orm_mode = True


class ReceievedTicketType(BaseModel):
    name: str
    price: float
    available: bool
    seated: bool
