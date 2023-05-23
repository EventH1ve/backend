from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from fastapi_sqlalchemy import db
from models.user import User as ModelUser
from models.event import Event as ModelEvent, UserEventBooking as ModelUserEventBooking
from models.admin import Admin as ModelAdmin
from schemas.dashboard import DashboardMetrics,DashboardMetricsAdmin
from schemas.event import DashboardEvent, DashboardEventAdmin
from lib.auth.jwt_bearer import getCurrentUserId
from datetime import datetime
from math import ceil
from sqlalchemy import and_


router = APIRouter()


@router.get('/', response_model=DashboardMetrics)
async def getDashboardMetrics(userId: Annotated[int, Depends(getCurrentUserId)]):
    createdAt = (db.session.query(ModelUser)
                 .with_entities(ModelUser.createdat, ModelUser.type).
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
    
    eventCount = (db.session.query(ModelEvent)
                  .join(ModelUserEventBooking, ModelEvent.id == ModelUserEventBooking.eventid)
                  .filter(ModelUserEventBooking.userid == userId)
                  .distinct(ModelEvent.name)
                  .count())

    membershipDuration = datetime.now() - createdAt

    return {
        "counters": {
            "upcomingEvents": len(upcomingEvents),
            "joinedEvents": eventCount,
            "membershipSince": f'{ceil(membershipDuration.total_seconds() / (60 * 60 * 24))} Days'
        },
        "upcomingEvents": parse_obj_as(List[DashboardEvent], upcomingEvents),
        "history": parse_obj_as(List[DashboardEvent], previousEvents)
    }


@router.get('/admin', response_model=DashboardMetricsAdmin)
async def getAdminDashboardMetrics(userId: Annotated[int, Depends(getCurrentUserId)]):
    membershipDuration = (db.session.query(ModelAdmin)
                          .with_entities(ModelAdmin.membershipend)
                          .filter(ModelAdmin.userid == userId).first())

    if not membershipDuration:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not an Admin.')

    (createdAt, membershipEndDate) = (db.session.query(ModelUser)
                 .with_entities(ModelUser.createdat, ModelAdmin.membershipend)
                 .join(ModelAdmin, and_(ModelAdmin.userid == ModelUser.id, ModelAdmin.userid == userId)).first())

    upcomingEvents = (db.session.query(ModelEvent)
                      .with_entities(
                        ModelEvent.id,
                        ModelEvent.name,
                        ModelEvent.venue,
                        ModelEvent.eventstartdatetime.label("date"),
                        )
                        .join(ModelAdmin, ModelEvent.adminid == ModelAdmin.id)
                        .filter(ModelAdmin.userid == userId, ModelEvent.eventstartdatetime > datetime.isoformat(datetime.now()))
                        .all())
    
    previousEvents = (db.session.query(ModelEvent)
                      .with_entities(
                        ModelEvent.id,
                        ModelEvent.name,
                        ModelEvent.venue,
                        ModelEvent.eventstartdatetime.label("date"),
                      )
                      .join(ModelAdmin, ModelEvent.adminid == ModelAdmin.id)
                      .filter(ModelAdmin.userid == userId, ModelEvent.eventstartdatetime <= datetime.isoformat(datetime.now()))
                      .all())
    
    membershipDuration = membershipEndDate - createdAt

    return {
        "counters": {
            "upcomingEvents": len(upcomingEvents),
            "pastEvents": len(previousEvents),
            "leftDaysforTheMembership": f'{ceil(membershipDuration.total_seconds() / (60 * 60 * 24))} Days'
        },
        "upcomingEvents": parse_obj_as(List[DashboardEventAdmin], upcomingEvents),
        "pastEvents": parse_obj_as(List[DashboardEventAdmin], previousEvents)
    } 


