from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class QueryAdmin(BaseModel):
    id: int
    name: str
    email: str
    phonenumber: str
    remainingQuantity: int

    class Config:
        orm_mode = True


class OwnerCounters(BaseModel):
    organizers: int
    attendees: int
    totalAccounts: int
    activeEvents: int
    transactionsProcessed: int


class OwnerMetrics(BaseModel):
    counters: OwnerCounters
    admins: List[QueryAdmin]


class OrganizerRequest(BaseModel):
    id: Optional[int]
    username: str
    password: str
    firstname: str
    lastname: str
    email: str
    phonenumber: str
    gender: str
    logo: str
    subscription: int


class UnapprovedAdmin(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    email: str