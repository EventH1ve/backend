import qrcode
from schemas.payment import PaymentInfo
import os
import cloudinary
from cloudinary.uploader import upload
from dotenv import load_dotenv
from uuid import UUID


"""
    Generates QRCode using the specified booking id and returns the path to 
    the generated image.
"""
def generateTicketQR(bookingId: UUID) -> str:
    qrImg = qrcode.make(bookingId)

    if not os.path.exists('tmp/'):
        os.mkdir('tmp')

    qrPath = f'tmp/{bookingId}.png'
    qrImg.save(qrPath)

    file = open(qrPath, "rb")
    res = upload(file, public_id=f'{bookingId}')
    file.close()

    return res.get('url')

