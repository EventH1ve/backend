from typing import List
from pydantic import BaseModel
from schemas.event import DashboardEvent,DashboardEventAdmin


class Counters(BaseModel):
    upcomingEvents: int
    joinedEvents: int
    membershipSince: str

class CountersForAdmin(BaseModel):
    upcomingEvents: int
    pastEvents: int
    leftDaysforTheMembership: str

class DashboardMetrics(BaseModel):
    counters: Counters
    upcomingEvents: List[DashboardEvent]
    history: List[DashboardEvent]

    class Config:
        orm_mode = True

class DashboardMetricsAdmin(BaseModel):
    Counters: CountersForAdmin
    UpcomingEvents: List[DashboardEventAdmin]
    PastEvents: List[DashboardEventAdmin]

    class Config:
        orm_mode = True
