from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    phonenumber: str
    firstname: str
    lastname: str
    type: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    username: str
    password: str
