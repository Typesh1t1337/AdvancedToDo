import os
import jwt
from dotenv import load_dotenv
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException

load_dotenv("../.env")
SECRET_KEY = os.getenv("JWT_SECRET")


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def compare_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_jwt_tokens(user_id: int) -> dict[str, str]:
    access_expire = datetime.utcnow() + timedelta(minutes=60)
    access_to_encode = {"sub": str(user_id), "exp": access_expire}

    refresh_expire = datetime.utcnow() + timedelta(days=30)
    refresh_to_encode = {"sub": str(user_id), "exp": refresh_expire}

    access_token = jwt.encode(access_to_encode, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_to_encode, SECRET_KEY, algorithm="HS256")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(detail="Token is expired", status_code=401)
    except jwt.InvalidTokenError:
        raise HTTPException(detail="Token is invalid", status_code=401)
