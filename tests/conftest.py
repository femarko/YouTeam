import pytest
import datetime
from typing import Optional

import sqlalchemy

import auth.entrypoints.flask_entrypoint
import orm_tool
from orm_tool import table_mapper


@pytest.fixture
def test_date():
    return datetime.datetime(1900, 1, 1)


def return_func_deco(func):
    def wrapper():
        return func
    return wrapper


@pytest.fixture(scope="function")
@return_func_deco
def fake_validate_func(**data):
    return data


@pytest.fixture(scope="function")
@return_func_deco
def fake_hash_pass_func(password: str):
    return password


@pytest.fixture(scope="function")
def fake_users_repo():
    return FakeUsersRepo


@pytest.fixture(scope="function")
def fake_advs_repo():
    return FakeAdvsRepo


@pytest.fixture(scope="function")
def fake_unit_of_work():
    return FakeUnitOfWork


@pytest.fixture(autouse=True, scope="session")
def start_mapping():
    table_mapper.start_mapping()


@pytest.fixture
def test_client():
    return auth.entrypoints.flask_entrypoint.flask_app.test_client()




@pytest.fixture
def test_user_data():
    return {"name": "test_name", "full_name": "test_full_name", "email": "test@email.test", "password": "test_pass"}


class FakeBaseRepo:
    def __init__(self, instances: list):
        self.instances: set = set(instances)
        self.temp_added = []
        self.temp_deleted = []

    def add(self, instance):
        self.temp_added.append(instance)

    def get(self, instance_id):
        if instance_id not in (instance.id for instance in self.instances):
            return []
        return next(instance for instance in self.instances if instance.id == instance_id)

    def delete(self, instance):
        self.temp_deleted.append(instance)

    def execute_adding(self):
        for item in self.temp_added:
            if not item.id:
                item.id = 1
            if not item.creation_date:
                item.creation_date = datetime.datetime(1900, 1, 1)
            self.instances.add(item)
        self.temp_added = []

    def execute_deletion(self):
        for item in self.temp_deleted:
            self.instances.remove(item)
        self.temp_deleted = []


class FakeUsersRepo(FakeBaseRepo):
    def __init__(self, users: list):
        super().__init__(instances=users)

    def __str__(self):
        return "FakeUsersRepo"


class FakeAdvsRepo(FakeBaseRepo):
    def __init__(self, advs: list):
        super().__init__(instances=advs)

    def __str__(self):
        return "FakeAdvsRepo"


class FakeUnitOfWork:
    def __init__(self, users: Optional[FakeUsersRepo] = None, advs: Optional[FakeAdvsRepo] = None):
        self.users = users
        self.advs = advs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()

    def rollback(self):
        pass

    def commit(self):
        if self.users and self.users.temp_added:
            self.users.execute_adding()
        if self.advs and self.advs.temp_added:
            self.advs.execute_adding()
        if self.users and self.users.temp_deleted:
            self.users.execute_deletion()
        if self.advs and self.advs.temp_deleted:
            self.advs.execute_deletion()


@pytest.fixture(scope="session")
def engine():
    return sqlalchemy.create_engine(orm_tool.POSTGRES_DSN)


@pytest.fixture
def session_maker(engine):
    return sqlalchemy.orm.sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def clear_db(engine):
    table_mapper.mapper.metadata.drop_all(bind=engine)
    table_mapper.mapper.metadata.create_all(bind=engine)
    yield
    table_mapper.mapper.metadata.drop_all(bind=engine)
    table_mapper.mapper.metadata.create_all(bind=engine)
