from pydantic import BaseModel
from datetime import datetime


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class UserProfile(BaseModel):
    name: str
    email: str
    created_at: datetime

