from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from schemas.dashboard import DashboardMetrics
from lib.auth.jwt_bearer import JWTBearer, getCurrentUserId


router = APIRouter()


@router.get('/', response_model=DashboardMetrics)
async def getDashboardMetrics(userId: Annotated[int, Depends(getCurrentUserId)]):
    return {
        "counters": {
            "upcomingEvents": 2,
            "joinedEvents": 10,
            "membershipSince": "2 months"
        }
    }

