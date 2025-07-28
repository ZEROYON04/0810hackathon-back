from fastapi import FastAPI

from app.app_settings import Settings, get_settings

settings: Settings = get_settings()
logger = settings.configure_logging()

app = FastAPI()


@app.get("/")
async def read_root() -> dict:
    logger.debug("This is debug message!")
    logger.info("Root endpoint accessed.")
    return {"message": f"Hello, {settings.APP_ENV}!"}
