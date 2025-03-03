import enum
from datetime import datetime
from typing import Optional, TypeVar


class Base:
    pass


class User(Base):
    def __init__(
            self,
            name: str,
            email: str,
            password: str,
            id: Optional[int] = None,
            full_name: Optional[str] = None,
            creation_date: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.name = name
        self.full_name = full_name,
        self.email = email
        self.password = password
        self.creation_date = creation_date


class UserColumns(str, enum.Enum):
    ID = "id",
    NAME = "name"
    EMAIL = "email"
    CREATION_DATE = "creation_date"


ModelClass = TypeVar("ModelClass", bound=Base)
