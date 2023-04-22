from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.user import User as ModelUser
from schemas.user import User


router = APIRouter()


@router.get('/', response_model=List[User])
async def user():
    user = db.session.query(ModelUser).all()
    return user
