from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    phoneNumber: str
    firstName: str
    lastName: str
    type: str


class User(UserBase):
    id: Optional[int] = None


class UserRead(UserBase):
    id: int
