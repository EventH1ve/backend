from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_sqlalchemy import db
from models.event import UserEventBooking as ModelUserEventBooking
from models.user import User as ModelUser
from schemas.payment import PaymentInfo
from schemas.event import ReceivedEvent, UserEventBooking
from lib.auth.jwt_bearer import getCurrentUserId
from lib.ticket.qrcode_handler import generateTicketQR


router = APIRouter()


@router.post('/')
async def createPaymentEntry(paymentInfo: PaymentInfo, userId: Annotated[int, Depends(getCurrentUserId)]):
    entry = (db.session.query(ModelUserEventBooking)
             .filter(ModelUserEventBooking.transactionid == paymentInfo.orderId).all())
    
    if entry:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Transaction already recorded.')
    
    entryModel = ModelUserEventBooking(**{'userid': userId, 'eventid': paymentInfo.eventId, 'price': paymentInfo.subtotal, 'transactionid': paymentInfo.orderId})

    db.session.add(entryModel)
    db.session.commit()

    return {
        "qrURL": generateTicketQR(userId, paymentInfo)
    }


@router.get('/user', response_model=List[UserEventBooking])
async def getUserPaidEvents(userId: Annotated[int, Depends(getCurrentUserId)]):
    user = (db.session.query(ModelUser)
                .filter(ModelUser.id == userId).first())

    return user.bookings


@router.post('/testcreateevent')
async def createPaymentEntry(receivedEvent: ReceivedEvent):
    for ticket in receivedEvent.tickets:
        print(ticket)

    return {
        "qrURL": "https://s.yimg.com/ny/api/res/1.2/yH3pHCBJenoyg5doW1sYqw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM5OQ--/https://media.zenfs.com/en-US/consequence_of_sound_458/316890984e9d434f684c7362a7f226b8"
    }