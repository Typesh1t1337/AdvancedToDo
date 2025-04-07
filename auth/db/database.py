from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(
    settings.database_connection,
    echo=True
)

AsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with engine.begin() as conn:
        yield conn