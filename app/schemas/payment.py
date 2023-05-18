from typing import List
from pydantic import BaseModel


class PaymentInfo(BaseModel):
    eventId: int
    orderId: str
    subtotal: float
    tickets: List[dict]

    class Config:
        orm_mode = True

