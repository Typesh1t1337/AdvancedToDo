from fastapi import Depends
from starlette import status
from starlette.responses import JSONResponse
from db.models import User
from schemas import RegisterUser, LoginUser
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from sqlalchemy import or_, select
from utils import hash_password, create_jwt_tokens, compare_password
from dependencies import auth_required

async def register(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    username = user.username
    email = user.email
    password = user.password

    if any(not value for value in [username, email, password]):
        return JSONResponse(
            {
                "error": "Username or Email or Password is empty",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    check_user = await db.execute(select(User).where(or_(User.email == email, User.name == username)))
    if check_user.scalars().first():
        return JSONResponse({
            "message": "Username already registered"
        }, status_code=status.HTTP_400_BAD_REQUEST)

    hashed_password = hash_password(password)
    new_user = User(
        name=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    tokens = create_jwt_tokens(new_user.id)

    return JSONResponse(tokens, status_code=status.HTTP_201_CREATED)


async def login(user: LoginUser, db: AsyncSession = Depends(get_db)):
    email = user.email
    password = user.password

    if not email or not password:
        return JSONResponse(
            {
                "error": "Email or Password is empty",
            }, status_code=status.HTTP_400_BAD_REQUEST
        )

    check_user = await db.execute(select(User).where(User.email == email))
    check_user = check_user.scalars().first()

    if not check_user:
        return JSONResponse({
            "error": "Username or Password is not correct",
        }, status_code=status.HTTP_400_BAD_REQUEST)

    if not compare_password(password=password, hashed_password=check_user.password):
        return JSONResponse({
            "error": "Username of Password is not correct",
        }, status_code=status.HTTP_400_BAD_REQUEST)

    token = create_jwt_tokens(check_user.id)

    return JSONResponse(token, status_code=status.HTTP_200_OK)


async def auth(user_id=Depends(auth_required)):
    return JSONResponse(
        {
            "token": user_id,
        }, status_code=status.HTTP_200_OK
    )
