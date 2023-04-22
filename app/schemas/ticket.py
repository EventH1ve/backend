from typing import Optional
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
    id: int
    eventid: int
    price: int

    class Config:
        orm_mode = True

