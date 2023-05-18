import os
import jwt
import time
from dotenv import load_dotenv

load_dotenv('.env')


JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']


"""
    Generates JWT token using the specified user id and returns it.
"""
def sign(userId: str) -> str:
    payload = {
        "user_id": userId,
        "expires": time.time() + 10000
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM).decode('utf-8')

    return str(token)


"""
    Verifies the provided JWT token.
    Returns true if token is valid
    Returns false if token is invalid
"""
def verify(token: str) -> bool:
    try:
        decodedToken = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True if decodedToken["expires"] >= time.time() else False
    except Exception as e:
        print(e)
        return False
    

"""
    Decodes the specified JWT token.
    Returns the user id if the token is valid, -1 otherwise. 
"""
def decodeToken(token: str) -> int:
    try:
        decodedToken = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decodedToken["user_id"]
    except Exception as e:
        return -1