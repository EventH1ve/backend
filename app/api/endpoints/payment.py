from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from schemas.payment import PaymentInfo
from schemas.event import ReceivedEvent
from schemas.ticket import ReceievedTicketType


router = APIRouter()


@router.post('/')
async def createPaymentEntry(paymentInfo: PaymentInfo):
    print(paymentInfo)

    return {
        "qrURL": "https://s.yimg.com/ny/api/res/1.2/yH3pHCBJenoyg5doW1sYqw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM5OQ--/https://media.zenfs.com/en-US/consequence_of_sound_458/316890984e9d434f684c7362a7f226b8"
    }

@router.post('/testcreateevent')
async def createPaymentEntry(receivedEvent: ReceivedEvent):
    for ticket in receivedEvent.tickets:
        print(ticket)

    return {
        "qrURL": "https://s.yimg.com/ny/api/res/1.2/yH3pHCBJenoyg5doW1sYqw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM5OQ--/https://media.zenfs.com/en-US/consequence_of_sound_458/316890984e9d434f684c7362a7f226b8"
    }