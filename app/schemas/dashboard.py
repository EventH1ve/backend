from typing import Optional, List
from pydantic import BaseModel
from schemas.event import DashboardEvent


class Counters(BaseModel):
    upcomingEvents: int
    joinedEvents: int
    membershipSince: str


class DashboardMetrics(BaseModel):
    counters: Counters
    upcomingEvents: List[DashboardEvent]
    history: List[DashboardEvent]

    class Config:
        orm_mode = True

