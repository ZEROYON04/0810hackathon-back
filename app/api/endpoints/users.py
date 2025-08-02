from fastapi import APIRouter

from app.app_settings import get_settings
from app.schema.user import UserResponse

router = APIRouter()

settings = get_settings()
logger = settings.configure_logging()


@router.post("/new-user")
async def create_user() -> UserResponse:
    user = UserResponse(user_id=1)  # Example user creation
    logger.info("Created new user: %s", user)
    return user
