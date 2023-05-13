import qrcode
from schemas.payment import PaymentInfo
import os
import cloudinary
from cloudinary.uploader import upload
from dotenv import load_dotenv

load_dotenv('.env')


CLOUDINARY_CLOUD_NAME = os.environ['CLOUDINARY_CLOUD_NAME']
CLOUDINARY_API_KEY = os.environ['CLOUDINARY_API_KEY']
CLOUDINARY_API_SECRET = os.environ['CLOUDINARY_API_SECRET']


cloudinary.config(
  cloud_name = CLOUDINARY_CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRET,
  secure = True
)

"""
    Generates QRCode for the given ticket and returns the path to 
    the generated image.
"""
def generateTicketQR(userId:int, booking: PaymentInfo) -> str:
    qrImg = qrcode.make(encodeBooking(userId, booking))

    if not os.path.exists('tmp/'):
        os.mkdir('tmp')

    qrPath = f'tmp/{booking.orderId}.png'
    qrImg.save(qrPath)

    file = open(qrPath, "rb")
    res = upload(file, public_id=f'{booking.orderId}')
    file.close()

    return res.get('url')


"""
    Encodes the payment information into a string for QRCode generation.
"""
def encodeBooking(userId: int, booking: PaymentInfo) -> str:
    return ';'.join([f'{userId}', f'{booking.eventId}', booking.orderId, f'{booking.subtotal}'])
