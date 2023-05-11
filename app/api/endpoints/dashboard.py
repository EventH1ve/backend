from typing import List, Annotated
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from fastapi_sqlalchemy import db
from models.user import User as ModelUser
from models.event import Event as ModelEvent, UserEventBooking as ModelUserEventBooking
from schemas.dashboard import DashboardMetrics
from schemas.event import DashboardEvent
from lib.auth.jwt_bearer import getCurrentUserId
from datetime import datetime
from math import ceil


router = APIRouter()


@router.get('/', response_model=DashboardMetrics)
async def getDashboardMetrics(userId: Annotated[int, Depends(getCurrentUserId)]):
    createdAt = (db.session.query(ModelUser)
                 .with_entities(ModelUser.createdat).
                 filter(ModelUser.id == userId).first())[0]

    upcomingEvents = (db.session.query(ModelEvent)
                      .with_entities(
                        ModelEvent.id,
                        ModelEvent.name,
                        ModelEvent.venue,
                        ModelEvent.eventstartdatetime.label("date"),
                        ModelUserEventBooking.price,
                        ModelUserEventBooking.transactionid,
                        ModelUserEventBooking.userid
                      )
                      .join(ModelUserEventBooking, ModelEvent.id == ModelUserEventBooking.eventid)
                      .filter(ModelUserEventBooking.userid == userId, ModelEvent.eventstartdatetime > datetime.isoformat(datetime.now()))
                      .all())
    
    previousEvents = (db.session.query(ModelEvent)
                      .with_entities(
                        ModelEvent.id,
                        ModelEvent.name,
                        ModelEvent.venue,
                        ModelEvent.eventstartdatetime.label("date"),
                        ModelUserEventBooking.price,
                        ModelUserEventBooking.transactionid
                      )
                      .join(ModelUserEventBooking, ModelEvent.id == ModelUserEventBooking.eventid)
                      .filter(ModelUserEventBooking.userid == userId, ModelEvent.eventstartdatetime <= datetime.isoformat(datetime.now()))
                      .all())
    
    membershipDuration = datetime.now() - createdAt

    return {
        "counters": {
            "upcomingEvents": len(upcomingEvents),
            "joinedEvents": len(upcomingEvents) + len(previousEvents),
            "membershipSince": f'{ceil(membershipDuration.total_seconds() / (60 * 60 * 24))} Days'
        },
        "upcomingEvents": parse_obj_as(List[DashboardEvent], upcomingEvents),
        "history": parse_obj_as(List[DashboardEvent], previousEvents)
    }

