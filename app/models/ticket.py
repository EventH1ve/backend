from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer)
    eventid = Column(Integer)
    qrcode = Column(Integer)
    seatnumber = Column(Integer)


class TicketType(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, index=True)
    eventid = Column(Integer)
    price = Column(Integer)
    