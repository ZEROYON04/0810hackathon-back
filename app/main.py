from fastapi import FastAPI

from app.api.endpoints import random_problems, users
from app.core.config import get_settings

settings = get_settings()
logger = settings.configure_logging()

app = FastAPI()

app.include_router(random_problems.router)
app.include_router(users.router)


@app.get("/")
async def read_root() -> dict:
    logger.debug("This is debug message test!")
    logger.info("Root endpoint accessed.")
    return {"message": f"Application environmet is {settings.APP_ENV}!"}
