from typing import Optional
from pydantic import BaseModel


class Admin(BaseModel):
    
    id: Optional[int] = None
    userid: int 

    class Config:
        orm_mode = True




