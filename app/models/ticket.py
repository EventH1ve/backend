from models import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship



eventTicketCapacity = Table(
    "eventticketcapacity",
    Base.metadata,
    Column("eventid", ForeignKey("event.id"), primary_key=True),
    Column("tickettypeid", ForeignKey("tickettype.id"), primary_key=True),
    Column("capacity", Integer),
    Column("reserved", Integer),
)

class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, ForeignKey("tickettype.id"))
    eventid = Column(Integer, ForeignKey("event.id"))
    qrcode = Column(Integer)
    seatnumber = Column(Integer)
    
    event = relationship("Event", back_populates="tickets")
    tickettype = relationship("TicketType", back_populates="ticket")


class TicketType(Base):
    __tablename__ = 'tickettype'
    id = Column(Integer, primary_key=True, index=True)
    eventid = Column(Integer, ForeignKey("event.id"))
    price = Column(Integer)

    event = relationship("Event", secondary=eventTicketCapacity, back_populates="tickettypes")
    ticket = relationship("Ticket", back_populates="tickettype")

