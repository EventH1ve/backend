import qrcode
import os
import cloudinary
from cloudinary.uploader import upload
from dotenv import load_dotenv
from uuid import UUID


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
