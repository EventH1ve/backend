from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from models.ticket import eventTicketCapacity
from models.admin import Admin
from sqlalchemy.sql import func
import uuid


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    profile = Column(String)
    adminid = Column(Integer, ForeignKey("admin.id"))
    datetime = Column(DateTime)
    venue = Column(String)
    description = Column(String)
    creationdate = Column(DateTime, server_default=func.now())

    type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    registrationstartdatetime = Column(DateTime, nullable=True)
    registrationenddatetime = Column(DateTime, nullable=True)
    eventstartdatetime = Column(DateTime, nullable=True)
    eventenddatetime = Column(DateTime, nullable=True)

    admin  = relationship("Admin", back_populates="events", uselist=False)
    tickets = relationship("Ticket", back_populates="event")
    tickettypes = relationship("TicketType", secondary=eventTicketCapacity, back_populates="event")


class UserEventBooking(Base):
    __tablename__ = 'usereventbooking'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userid = Column(Integer, ForeignKey("users.id"))
    eventid = Column(Integer, ForeignKey("event.id"))
    bookingdate = Column(DateTime, server_default=func.now())
    price = Column(Float)
    transactionid = Column(String)
    tickettype = Column(String)

    users = relationship("User", back_populates="bookings")
    event = relationship("Event")

    