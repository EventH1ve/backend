from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from lib.auth.jwt_bearer import getCurrentUserId
from models.event import Event as ModelEvent, UserEventBooking
from models.ticket import TicketType as ModelTicketType, Ticket as ModelTicket
from models.admin import Admin as ModelAdmin
from models.user import User as ModelUser
from schemas.event import Event, ListEvent, SingleEvent, AdminEvent as ModelAdminEvent

router = APIRouter()
