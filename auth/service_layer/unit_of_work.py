from sqlalchemy.exc import IntegrityError

from domain import custom_errors
from orm import session_maker
from repository.repository import RepoProto, UserRepository


class UnitOfWork:
    def __init__(self):
        self.session_maker = session_maker

    def __enter__(self):
        self.session = self.session_maker()
        self.users: RepoProto = UserRepository(
            session=self.session, db_errors={IntegrityError: custom_errors.AlreadyExistsError}
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            if self.users.db_errors is None:
                raise custom_errors.InternalServerError
            else:
                raise self.users.db_errors.get(type(e), custom_errors.InternalServerError)
