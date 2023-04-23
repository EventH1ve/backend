from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


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

  
class VenueRestriction(Base):
    __tablename__ = 'venuerestriction'
    id = Column(Integer, primary_key=True, index=True)
    venueid = Column(Integer)
    restriction = Column(String)  


class VenueContact(Base):
    __tablename__ = 'venuecontact'
    id = Column(Integer, primary_key=True, index=True)
    venueid = Column(Integer)
    contactid = Column(Integer)


class ContactPerson(Base):
    __tablename__ = 'contactperson'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phonenumber = Column(String)
    