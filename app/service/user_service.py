from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.crud.user import UserCRUD
from app.schema.user import UserCreate, UserResponse

logger = get_settings().configure_logging()


def create_user(db: Session) -> UserResponse:
    """Create a new user in the database."""
    logger.debug("Creating user")
    user_crud = UserCRUD(db)
    user_data = UserCreate()  # 空のユーザーデータを作成
    try:
        db_user = user_crud.create(user_data)
        logger.info("User created successfully: %s", db_user)
        return UserResponse(
            user_id=db_user.user_id,
        )
    except Exception:
        logger.exception("Error in creating user")
        raise
