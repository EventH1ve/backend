from models import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    gender = Column(String)
    phonenumber = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    type = Column(String)
    createdat = Column(DateTime, server_default=func.now())

    admin = relationship('Admin', back_populates='user', uselist=False)

    bookings = relationship("UserEventBooking", back_populates="users")
