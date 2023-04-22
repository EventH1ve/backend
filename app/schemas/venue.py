from typing import Optional
from pydantic import BaseModel


class Venue(BaseModel):
    id: Optional[int] = None
    name: str
    capacity: int
    description: str
    createdby: str
    buildingnumber: int
    streetname: str
    city: str
    country: str

    class Config:
        orm_mode = True


class VenueRestriction(BaseModel):
    id: Optional[int] = None
    venueid: int
    restriction: str

    class Config:
        orm_mode = True

class ContactPerson(BaseModel):
    id: Optional[int] = None
    name: str
    phonenumber: str

    class Config:
        orm_mode = True
