import jwt
from dotenv import load_dotenv
import os

from fastapi import HTTPException

load_dotenv("../.env")

SECRET_KEY =os.getenv("JWT_SECRET")
def decode_jwt(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")