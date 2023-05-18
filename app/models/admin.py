from models import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"), unique=True)
    membershipend = Column(DateTime, default=datetime.datetime.now() + datetime.timedelta(days=120)) # 4 month membership by default

    user = relationship("User", back_populates="admin")
    events = relationship("Event", back_populates="admin")
