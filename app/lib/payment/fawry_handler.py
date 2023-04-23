import requests
import hashlib
import json
from app.main import PROJECT_ENV
from app.schemas.ticket import Ticket, TicketType
from app.schemas.user import User, UserCreditCard

# Fawry endpoint 
STAGING_ENDPOINT="https://atfawry.fawrystaging.com/ECommerceWeb/Fawry/payments/charge"
PROD_ENDPOINT="https://www.atfawry.com/ECommerceWeb/Fawry/payments/charge"
FAWRY_ENDPOINT = PROD_ENDPOINT if PROJECT_ENV == "prod" else STAGING_ENDPOINT

# Merchant info
MERCHANT_CODE='merchant_code'
MERCHANT_REF_NUM='refNum'
MERCHANT_SECURITY_KEY="securityKey"


"""
    Constructs and sends the payment request to the fawry endpoint.
    Returns the transaction's auth number if successful, otherwise returns an empty string.
"""
def sendPaymentRequest(user: User, userCreditCard: UserCreditCard, ticket: Ticket, ticketType: TicketType) -> str:
    # Payment Data
    merchantCode = MERCHANT_CODE
    merchantRefNum = MERCHANT_REF_NUM
    payment_method = 'CARD'
    amount = f'{ticketType.price}'
    cardNumber = f'{userCreditCard.cardnumber}'
    cardExpiryYear = f'{userCreditCard.cardexpiryyear}'
    cardExpiryMonth = f'{userCreditCard.cardexpirymonth}'
    cvv = f'{userCreditCard.cvv}'
    returnUrl = "https://developer.fawrystaging.com"
    merchant_sec_key = MERCHANT_SECURITY_KEY

    # Generating signature
    card_info = ""
    card_info = card_info +  (merchantCode  + merchantRefNum + payment_method +
                    amount + cardNumber + cardExpiryYear + cardExpiryMonth + cvv +returnUrl+ merchant_sec_key)
    signature = hashlib.sha256(str(card_info).encode('utf-8')).hexdigest()

    # JSON request
    paymentData = {
        "merchantCode": merchantCode,
        "merchantRefNum": merchantRefNum,
        "cardNumber": cardNumber,
        "cardExpiryYear": cardExpiryYear,
        "cardExpiryMonth": cardExpiryMonth,
        "cvv": cvv,
        "customerMobile": user.phonenumber,
        "customerEmail": user.email,
        "amount": ticketType.price,
        "currencyCode": "EGP",
        "language" : "en-gb",
        "returnUrl": returnUrl,
        "chargeItems" : [
            {
                "itemId": f'{ticket.id}',
                "price": ticketType.price,
                "quantity": 1
            }
        ],
        "paymentMethod": "CARD",
        "signature": signature
    }
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json'}
    res = requests.post(FAWRY_ENDPOINT, json.dumps(paymentData), headers = headers)
    res = res.json()
    return res['authNumber'] if res['statusCode'] == 200 else ""