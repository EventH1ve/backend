from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from schemas.ticket import Ticket, TicketType
from models.ticket import Ticket as ModelTicket, TicketType as ModelTicketType


router = APIRouter()


@router.post('/type')
async def createTicketType(ticketType: TicketType):
    ticketTypeModel = ModelTicketType(**ticketType.dict())

    db.session.add(ticketTypeModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Ticket type created."
    }


@router.get('/type', response_model=List[TicketType])
async def listTicketTypes():
    ticketTypes = db.session.query(ModelTicketType).all()
    return ticketTypes