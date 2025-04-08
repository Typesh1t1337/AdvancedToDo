from fastapi import APIRouter
from api import upload_task

class TaskRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/tasks", tags=["tasks"])
        self.add_routes()

    def add_routes(self):
        self.router.add_api_route("/upload", upload_task, methods=["POST"])


task_router = TaskRouter()