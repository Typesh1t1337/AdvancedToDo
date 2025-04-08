from fastapi import APIRouter
from api import register, login, profile
from schemas import UserProfile

class AuthRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.add_routes()

    def add_routes(self):
        self.router.add_api_route("/register", register, methods=["POST"])
        self.router.add_api_route("/login", login, methods=["POST"])
        self.router.add_api_route("/profile", profile, methods=["GET"], response_model=UserProfile)



auth_router = AuthRouter()