from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import func
from models.event import Event as ModelEvent
from models.venue import Venue as ModelVenue
from models.ticket import TicketType as ModelTicketType
from schemas.event import Event, ListEvent, SingleEvent


router = APIRouter()


@router.get('/')
async def getDashboardMetrics():
    return {
        "message": "Success"
    }

