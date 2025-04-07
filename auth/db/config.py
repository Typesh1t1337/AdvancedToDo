from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv("../../.env")


class DbConfig(BaseSettings):
    AUTH_DB_PASSWORD: str
    AUTH_DB_USER: str
    AUTH_DB_DB: str

    @property
    def database_connection(self) -> str:
        return (
            f"postgresql+asyncpg://{self.AUTH_DB_USER}:{self.AUTH_DB_PASSWORD}"
            f"@auth_postgres:5432/{self.AUTH_DB_DB}"
        )

    class Config:
        env_file = "../../.env"
        extra = "allow"


settings = DbConfig()


