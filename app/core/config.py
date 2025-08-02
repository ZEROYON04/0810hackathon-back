import logging
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "development"
    MAPS_API_KEY: str
    DATABASE_URL: str

    def configure_logging(self) -> logging.Logger:
        logger = logging.getLogger("uvicorn")

        if self.APP_ENV == "development":
            Path("app/logs").mkdir(exist_ok=True)
            handler = logging.FileHandler("app/logs/app.log")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
            )
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

        return logger


@lru_cache
def get_settings() -> Settings:
    return Settings()
