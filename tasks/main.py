from fastapi import FastAPI
from db.models import Base
from db.database import engine
from routes import task_router

app = FastAPI()
app.include_router(task_router.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)