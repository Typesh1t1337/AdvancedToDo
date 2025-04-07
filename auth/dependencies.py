from fastapi import Request, HTTPException
from utils import decode_jwt


def auth_required(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    token = token[7:]
    return decode_jwt(token)
