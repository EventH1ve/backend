import qrcode
import os
import cloudinary
from cloudinary.uploader import upload
from dotenv import load_dotenv
from uuid import UUID
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

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

    generate_ticket(f'tmp/{bookingId}.png', "https://res.cloudinary.com/dacn7ee03/image/upload/v1684773729/gqpmwkvwpolvnlt4nkfl.jpg", bookingId, qr_size=(500, 500), qr_position=(2024, 176))

    file = open(f'tmp/{bookingId}1.png', "rb")
    res = upload(file, public_id=f'{bookingId}')
    file.close()

    return res.get('url')


def generate_ticket(qr_image, template_image_url, bookingId, qr_size=(500, 500), qr_position=(2024, 176), color="black", fontsize=25):
    
    response = requests.get(template_image_url)
    template_image = Image.open(BytesIO(response.content))

    qr_image = Image.open(qr_image)
    qr_image = qr_image.resize(qr_size)
    ticket_image = template_image.copy()
    ticket_image.paste(qr_image, qr_position)

    draw = ImageDraw.Draw(ticket_image)
    font = ImageFont.truetype("arial.ttf", size=fontsize)
    text_width, text_height = draw.textsize("ticket_id", font=font)
    text_x = qr_position[0] + qr_size[0] // 2 - text_width // 2
    text_y = qr_position[1] + qr_size[1] + 10

    ticket_image.save(f'tmp/{bookingId}1.png')
