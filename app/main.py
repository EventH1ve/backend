import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from api.api import api_router
from dotenv import load_dotenv

load_dotenv('.env')

PROJECT_ENV = os.environ['PROJECT_ENV']

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(request.method, request.url)
    response = await call_next(request)
    return response


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["home"])
def greet():
    return {"success": True}


app.include_router(api_router)
