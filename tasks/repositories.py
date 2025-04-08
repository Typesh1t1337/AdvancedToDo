from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UploadTask
from db.models import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_task(self, task: UploadTask, user_id) -> Task:
        result = Task(**task.dict(), user_id=int(user_id))

        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result



