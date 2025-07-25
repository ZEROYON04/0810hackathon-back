import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    APP_ENV: str = "development"
    MAPS_API_KEY: str

    def configure_logging(self):
        logger = logging.getLogger("uvicorn")

        if self.APP_ENV == "development":
            logging.basicConfig(level=logging.DEBUG)
            os.makedirs("app/logs", exist_ok=True)
            handler = logging.FileHandler("app/logs/app.log")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

        return logger

@lru_cache()
def get_settings():
    return Settings()
