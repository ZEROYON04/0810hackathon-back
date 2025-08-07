from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseCRUD(ABC):
    """Base class for CRUD operations."""

    def __init__(self, db: Session) -> None:
        """Initialize with a database session."""
        if not isinstance(db, Session):
            raise InvalidDBSessionError
        if db is None:
            raise ValueError
        self.db = db

    @abstractmethod
    def create(self, data: object) -> object:
        """Create a new record."""

    @abstractmethod
    def read(self, record_id: int) -> object | None:
        """Read a record by its ID."""


class InvalidDBSessionError(TypeError):
    """Exception raised when the DB session is invalid."""

    def __init__(self, message: str = "db must be an instance of sqlalchemy.orm.Session") -> None:
        super().__init__(message)
