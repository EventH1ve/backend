from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.user import User as ModelUser
from schemas.user import User, LoginUser
import bcrypt
import lib.auth.auth_handler as authHandler


router = APIRouter()


@router.get('/', response_model=List[User])
async def user():
    user = db.session.query(ModelUser).all()
    return user


@router.post('/signup')
async def signup(user: User):
    query = db.session.query(ModelUser).filter(ModelUser.username == user.username).first()
    
    if query:
        return {
            "success": False,
            "message": "Username already exists."
        }
    
    user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    userModel = ModelUser(**user.dict())

    db.session.add(userModel)
    db.session.commit()

    return {
        "success": True,
        "message": "User created."
    }


@router.get('/login')
async def login(user: LoginUser):
    query = db.session.query(ModelUser).filter(ModelUser.username == user.username).first()

    invalidResponse = {
        "success": False,
        "message": "Invalid credentials."
    }

    if not query:
        return invalidResponse
    
    if not bcrypt.checkpw(user.password.encode('utf-8'), query.password.encode('utf-8')):
        return invalidResponse

    return {
        "success": True,
        "message": "Login successful.",
        "accessToken": authHandler.sign(query.id)
    }


@router.get('/verifyToken')
async def verifyToken(token: str):
    res = authHandler.verify(token)

    invalidResponse = {
        "success": False,
        "message": "Invalid token."
    }

    if not res or res == "":
        return invalidResponse
    
    return {
        "success": True,
        "message": "Token validation successful."
    }
