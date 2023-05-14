from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_sqlalchemy import db
from models.event import UserEventBooking as ModelUserEventBooking
from models.user import User as ModelUser
from schemas.payment import PaymentInfo
from schemas.event import ReceivedEvent, UserEventBooking
from lib.auth.jwt_bearer import getCurrentUserId
from lib.ticket.qrcode_handler import generateTicketQR
from dotenv import load_dotenv
import os
from twilio.rest import Client


load_dotenv('.env')
router = APIRouter()


TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

twilioClient = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


@router.post('/')
async def createPaymentEntry(paymentInfo: PaymentInfo, userId: Annotated[int, Depends(getCurrentUserId)]):
    entry = (db.session.query(ModelUserEventBooking)
             .filter(ModelUserEventBooking.transactionid == paymentInfo.orderId).all())
    
    if entry:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Transaction already recorded.')
    
    entryModel = ModelUserEventBooking(**{'userid': userId, 'eventid': paymentInfo.eventId, 'price': paymentInfo.subtotal, 'transactionid': paymentInfo.orderId})

    db.session.add(entryModel)
    db.session.commit()

    qrURL = generateTicketQR(userId, paymentInfo)

    userPhoneNumber = (db.session.query(ModelUser)
                       .with_entities(ModelUser.phonenumber)
                       .filter(ModelUser.id == userId).first())

    twilioClient.messages.create(
        to=f"whatsapp:+2{userPhoneNumber[0]}",
        from_="whatsapp:+14155238886",
        body=f'Thank you for using EventHive!\n\nYour order ID is {paymentInfo.orderId}\n\nYour ticket\'s QR Code can be accessed on the following link: {qrURL}\n\nEnjoy your event!')

    return {
        "qrURL": qrURL
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