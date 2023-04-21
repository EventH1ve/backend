import uvicorn
import os
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from models.user import User as ModelUser
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/", tags=["home"])
def greet():
    return {"success": True}


@app.get('/user/')
async def user():
    user = db.session.query(ModelUser).all()
    return user
