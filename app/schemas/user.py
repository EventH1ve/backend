from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    gender: str
    phonenumber: str
    firstname: str
    lastname: str
    type: str
    createdat: Optional[datetime]

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    username: str
    password: str
