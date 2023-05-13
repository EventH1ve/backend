from typing import Optional
from pydantic import BaseModel


class Partner(BaseModel):
    id: Optional[int] = None
    name: str
    img:str

    class Config:
        orm_mode = True


