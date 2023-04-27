from typing import Optional
from pydantic import BaseModel


class Event(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    type: str
    status: str
    creationdate: Optional[str]
    registrationstartdatetime = str
    registrationenddatetime = str
    eventstartdatetime = str
    eventenddatetime = str
    venueid: int
    profile: str

    class Config:
        orm_mode = True


class ClientEvent(BaseModel):
    id: int
    name: str
    venue: str
    date: str
    price: str
    profile: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    username: str
    password: str
