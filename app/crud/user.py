from app.core.config import get_settings
from app.crud.base import BaseCRUD
from app.model.generated_models import Users
from app.schema.user import UserCreate

logger = get_settings().configure_logging()


class UserCRUD(BaseCRUD):
    def create(self, data: UserCreate) -> Users:
        """Create a new user in the database."""
        db_user = Users(**data.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def read(self, user_id: int) -> Users | None:
        """Read a user by their user_id."""
        logger.debug("Reading user with ID: %s", user_id)
        return self.db.query(Users).filter(Users.user_id == user_id).first()
