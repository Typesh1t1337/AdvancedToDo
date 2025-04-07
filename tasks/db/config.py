from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Dbconfig(BaseSettings):
    TASK_DB_PASSWORD: str
    TASK_DB_USER: str
    TASK_DB_DB: str

    @property
    def database_connection(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TASK_DB_USER}:{self.TASK_DB_PASSWORD}"
            f"@localhost:5434/{self.TASK_DB_USER}"
        )

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Dbconfig()