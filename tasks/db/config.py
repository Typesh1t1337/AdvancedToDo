from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv("../../.env")

class Dbconfig(BaseSettings):
    TASK_DB_PASSWORD: str
    TASK_DB_USER: str
    TASK_DB_DB: str

    @property
    def database_connection(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TASK_DB_USER}:{self.TASK_DB_PASSWORD}"
            f"@tasks_postgres:5432/{self.TASK_DB_DB}"
        )

    class Config:
        env_file = "../../.env"
        extra = "allow"


settings = Dbconfig()