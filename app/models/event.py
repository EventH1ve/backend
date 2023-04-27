from models import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.ticket import eventTicketCapacity



class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    status = Column(String)
    creationdate = Column(DateTime)
    registrationstartdatetime = Column(DateTime)
    registrationenddatetime = Column(DateTime)
    eventstartdatetime = Column(DateTime)
    eventenddatetime = Column(DateTime)

    tickets = relationship("Ticket", back_populates="event")
    tickettypes = relationship("TicketType", secondary=eventTicketCapacity, back_populates="event")