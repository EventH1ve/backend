from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.ticket import eventTicketCapacity
from models.admin import Admin
from sqlalchemy.sql import func


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    venue = Column(String)
    type = Column(String)
    status = Column(String)
    creationdate = Column(DateTime, server_default=func.now())
    registrationstartdatetime = Column(DateTime)
    registrationenddatetime = Column(DateTime)
    eventstartdatetime = Column(DateTime)
    eventenddatetime = Column(DateTime)
    profile = Column(String)
    adminid = Column(Integer,ForeignKey("admin.id"))

    admin  = relationship("Admin", back_populates="events", uselist=False)
    tickets = relationship("Ticket", back_populates="event")
    tickettypes = relationship("TicketType", secondary=eventTicketCapacity, back_populates="event")


class UserEventBooking(Base):
    __tablename__ = 'usereventbooking'
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"))
    eventid = Column(Integer, ForeignKey("event.id"))
    bookingdate = Column(DateTime, server_default=func.now())
    price = Column(Float)
    transactionid = Column(String)

    users = relationship("User", back_populates="bookings")
