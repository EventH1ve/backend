from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Admin(BaseModel):
    
    id: Optional[int] = None
    userid: int 
    membershipend: datetime

    class Config:
        orm_mode = True




