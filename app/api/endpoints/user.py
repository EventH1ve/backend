from typing import List
from fastapi import APIRouter, status, HTTPException
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists.')
    
    user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    userModel = ModelUser(**user.dict())

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
async def login(loginUser: LoginUser):
    user = db.session.query(ModelUser).filter(ModelUser.username == loginUser.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    
    if not bcrypt.checkpw(loginUser.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')

    if user.type == 'admin':
        unapproved = db.session.query(ModelAdmin).filter(user.id == ModelAdmin.userid, ModelAdmin.active.is_(False)).first()
        if unapproved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unapproved organizer.')

    return {
        "success": True,
        "message": "Login successful.",
        "id": user.id,
        "role": user.type.lower(),
        "username": user.username,
        "email": user.email,
        "firstName": user.firstname,
        "lastName": user.lastname,
        "mobileNumber": user.phonenumber,
        "gender": user.gender,
        "token": authHandler.sign(user.id)
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
