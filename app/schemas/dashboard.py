from typing import Optional
from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    id: int
    type: int
    eventid: int
    qrcode: str
    seatnumber: int

    class Config:
        orm_mode = True
