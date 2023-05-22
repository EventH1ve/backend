from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Admin(BaseModel):
    
    id: Optional[int] = None
    userid: int 
    membershipend: datetime
    active: Optional[bool]

    class Config:
        orm_mode = True




