from models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    phonenumber = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    type = Column(String)
    
    bookings = relationship("UserEventBooking", back_populates="users")