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
            creation_date: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.creation_date = creation_date


ModelClass = TypeVar("ModelClass", bound=Base)
