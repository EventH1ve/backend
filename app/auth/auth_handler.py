from typing import Dict
import os
import jwt
import time
from dotenv import load_dotenv

load_dotenv('.env')


JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']


def sign(userId: str) -> str:
    payload = {
        "user_id": userId,
        "expires": time.time() + 600
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return str(token)


def verify(token: str) -> str:
    try:
        decodedToken = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return str(decodedToken) if decodedToken["expires"] >= time.time() else None
    except:
        return ""
    