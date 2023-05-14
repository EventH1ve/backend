from models import Base
from sqlalchemy import Column, Integer, String

# Base = declarative_base()

class Partner(Base):
    __tablename__ = 'partner'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    img = Column(String)
