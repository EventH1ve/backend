from models import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
import datetime

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"), unique=True)
    membershipend = Column(DateTime, default=datetime.datetime.now() + datetime.timedelta(days=120)) # 4 months membership by default
    active = Column(Boolean, default=False)
    logo = Column(String)

    user = relationship("User", back_populates="admin")
    events = relationship("Event", back_populates="admin")
