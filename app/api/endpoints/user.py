from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.user import User as ModelUser
from schemas.user import User, LoginUser
from models.admin import Admin as ModelAdmin
import bcrypt
import lib.auth.auth_handler as authHandler


router = APIRouter()


@router.get('/', response_model=List[User])
async def user():
    users = db.session.query(ModelUser).all()
    return users


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


    # check if the type == admin do a query to add that user id in admin Table

    db.session.add(userModel)
    db.session.commit()
    
    if user.type.lower() == "admin":
        adminModel = ModelAdmin(userid=userModel.id)
        db.session.add(adminModel)
        db.session.commit()

    return {
        "success": True,
        "message": "User created."
    }


@router.post('/login')
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
        "token": authHandler.sign(query.id)
    }


@router.post('/verifyToken')
async def verifyToken(token: str):

    invalidResponse = {
        "success": False,
        "message": "Invalid token."
    }

    if not authHandler.verify(token):
        return invalidResponse
    
    return {
        "success": True,
        "message": "Token validation successful."
    }
