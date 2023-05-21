from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_sqlalchemy import db
from models.event import UserEventBooking as ModelUserEventBooking
from models.user import User as ModelUser
from models.ticket import TicketType as ModelTicketType
from schemas.payment import PaymentInfo
from schemas.event import UserEventBooking
from schemas.ticket import TicketType
from lib.auth.jwt_bearer import getCurrentUserId
from lib.ticket.qrcode_handler import generateTicketQR
from lib.ticket.seat_handler import bookSeats
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
    
    ticketLinks = list()

    for order in paymentInfo.tickets:
        for _ in range(order['count']):
            entryModel = ModelUserEventBooking(**{'userid': userId, 'eventid': paymentInfo.eventId, 'price': paymentInfo.subtotal, 'transactionid': paymentInfo.orderId, 'tickettype': order['ticket_type']})

            db.session.add(entryModel)
            db.session.commit()

            qrURL = generateTicketQR(entryModel.id)
            ticketLinks.append(qrURL)

            userPhoneNumber = (db.session.query(ModelUser)
                            .with_entities(ModelUser.phonenumber)
                            .filter(ModelUser.id == userId).first())

            twilioClient.messages.create(
                to=f"whatsapp:+2{userPhoneNumber[0]}",
                from_="whatsapp:+14155238886",
                body=f'Thank you for using EventHive!\n\nYour order ID is {paymentInfo.orderId}\n\nYour ticket type is {order["ticket_type"]}\n\nYour ticket\'s QR Code can be accessed on the following link: {qrURL}\n\nEnjoy your event!')

        # Mark booked seats
        ticketType = (db.session.query(ModelTicketType)
                    .filter(ModelTicketType.eventid == paymentInfo.eventId, ModelTicketType.name == order['ticket_type'])
                    .first())
        
        bookSeats(order['seats'], ticketType)
        
        (db.session.query(ModelTicketType)
        .filter(ModelTicketType.eventid == paymentInfo.eventId, ModelTicketType.name == order['ticket_type'])
        .update({ModelTicketType.seats: ticketType.seats}))

    db.session.commit()

    return {
        "qrURL": ticketLinks
    }


@router.get('/user', response_model=List[UserEventBooking])
async def getUserPaidEvents(userId: Annotated[int, Depends(getCurrentUserId)]):
    user = (db.session.query(ModelUser)
                .filter(ModelUser.id == userId).first())

    return user.bookings
