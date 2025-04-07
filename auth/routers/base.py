from fastapi import APIRouter

class BaseRouter:
    def __init__(self, prefix:str, tag:str):
        self.router = APIRouter(prefix=prefix, tags=[tag])
        self.add_routes()

    def add_routes(self):
        pass