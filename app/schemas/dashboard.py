from typing import Optional
from pydantic import BaseModel


class Counters(BaseModel):
    upcomingEvents: int
    joinedEvents: int
    membershipSince: str


class DashboardMetrics(BaseModel):
    counters: Counters

    class Config:
        orm_mode = True

