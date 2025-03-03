from typing import Protocol, Any, Optional

from domain import models, custom_errors


class RepoProto(Protocol):
    def __init__(self, session, db_errors=None):
        self.session = session
        self.db_errors = db_errors

    def add(self, instance) -> None:
        pass

    def get(self, instance_id: int) -> Any:
        pass

    def delete(self, instance) -> None:
        pass


class Repository:
    def __init__(self, session, db_errors: Optional[dict] = None):
        if db_errors is None:
            db_errors = {}
        self.session = session
        self.model_cl = None
        self.db_errors = db_errors

    def add(self, instance) -> None:
        try:
            self.session.add(instance)
        except Exception as e:
            if self.db_errors is None:
                raise custom_errors.InternalServerError
            else:
                raise self.db_errors.get(e, custom_errors.InternalServerError)

    def get(self, instance_id: int) -> Any:
        return self.session.get(self.model_cl, instance_id)

    def delete(self, instance) -> None:
        self.session.delete(instance)


class UserRepository(Repository):
    def __init__(self, session, db_errors=None):
        super().__init__(session=session, db_errors=db_errors)
        self.model_cl = models.User
