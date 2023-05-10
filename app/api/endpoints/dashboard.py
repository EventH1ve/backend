from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import func
from schemas.dashboard import DashboardMetrics


router = APIRouter()


@router.get('/', response_model=DashboardMetrics)
async def getDashboardMetrics():
    return {
        "counters": {
            "upcomingEvents": 2,
            "joinedEvents": 10,
            "membershipSince": "2 months"
        }
    }

