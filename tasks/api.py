from fastapi import Depends
from starlette.responses import JSONResponse
from starlette import status
from dependencies import auth_required
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas import UploadTask
from celery_worker import recognize_category
from repositories import TaskRepository


async def upload_task(task: UploadTask,
                      user_id=Depends(auth_required),
                      db: AsyncSession = Depends(get_db)
                      ):
    try:
        repo = TaskRepository(db)
        result = await repo.add_task(task=task, user_id=user_id)

        recognize_category.delay(result.description, task_id=result.id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "Task uploaded!",
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": str(e)
        })
