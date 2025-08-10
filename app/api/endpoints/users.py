from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.schema.user import UserResponse
from app.service.user_service import create_user as create_user_service

router = APIRouter(prefix="/user", tags=["User"])

settings = get_settings()
logger = settings.configure_logging()


@router.post(
    "/new-user",
    summary="新しいユーザーを作成するAPIエンドポイント。",
    description="作成中のため、現時点ではダミーのユーザー情報(user_id=1)の固定値を返します。",
)
async def create_user(db: Annotated[Session, Depends(get_db)]) -> UserResponse:
    """Create a new user and return the user response."""
    user = create_user_service(db)
    logger.info("Created new user: %s", user)
    return user
