from models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Venue(Base):
    __tablename__ = 'venue'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    capacity = Column(Integer)
    description = Column(String)
    createdby = Column(String)
    buildingnumber = Column(Integer)
    streetname = Column(String)
    city = Column(String)
    country = Column(String)

    events = relationship("Event", back_populates="venue")

  
class VenueRestriction(Base):
    __tablename__ = 'venuerestriction'
    id = Column(Integer, primary_key=True, index=True)
    venueid = Column(Integer, ForeignKey("venue.id"))
    restriction = Column(String)  


class VenueContact(Base):
    __tablename__ = 'venuecontact'
    id = Column(Integer, primary_key=True, index=True)
    venueid = Column(Integer, ForeignKey("venue.id"))
    contactid = Column(Integer, ForeignKey("contactperson.id"))


class ContactPerson(Base):
    __tablename__ = 'contactperson'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phonenumber = Column(String)
    