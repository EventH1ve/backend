from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import func


router = APIRouter()


@router.get('/')
async def getDashboardMetrics():
    return {
        "message": "Success"
    }

