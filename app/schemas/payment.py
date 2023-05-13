from typing import Optional, List
from pydantic import BaseModel
from schemas.event import DashboardEvent


class PaymentInfo(BaseModel):
    eventId: int
    orderId: str
    subtotal: float
    tickets: List[dict]

    class Config:
        orm_mode = True

