from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    phoneNumber: str
    firstName: str
    lastName: str
    type: str

    class Config:
        orm_mode = True
