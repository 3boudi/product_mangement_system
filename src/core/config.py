from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
settings = Settings()