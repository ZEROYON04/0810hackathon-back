from fastapi import APIRouter

from app.core.config import get_settings
from app.schema.user import UserResponse

router = APIRouter()

settings = get_settings()
logger = settings.configure_logging()


@router.post(
    "/new-user",
    summary="新しいユーザーを作成するAPIエンドポイント。",
    description="作成中のため、現時点ではダミーのユーザー情報(user_id=1)の固定値を返します。",
)
async def create_user() -> UserResponse:
    user = UserResponse(user_id=1)  # Example user creation
    logger.info("Created new user: %s", user)
    return user
