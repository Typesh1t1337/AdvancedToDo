from fastapi import Request, HTTPException
from utils import decode_jwt

def auth_required(req:Request):
    token = req.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        raise HTTPException(status_code=401)

    token = token[7:]

    return decode_jwt(token)

