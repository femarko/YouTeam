import pytest

from auth.service_layer import unit_of_work, manager
from auth.validation_and_pass_hashing import pass_hashing, validation
from auth.entrypoints.flask_entrypoint import views


@pytest.fixture
def create_user_(clear_db, test_client, test_user_data):
    test_client.post("http://127.0.0.1:5000/users/", json=test_user_data)


def test_create_user(test_client, clear_db):
    user_data = {
        "name": "test_name", "full_name": "test_full_name", "email": "test@email.com", "password": "test_password"
    }
    response = test_client.post("http://127.0.0.1:5000/users/", json=user_data)
    uow = unit_of_work.UnitOfWork()
    with uow:
        user_from_repo = uow.users.get_by_id(instance_id=response.json["New user is created"]["id"])
    assert response.status_code == 201
    assert response.json["New user is created"]["id"] == user_from_repo.id
    assert response.json["New user is created"]["name"] == user_from_repo.name == user_data["name"]
    assert response.json["New user is created"]["full_name"] == user_from_repo.full_name == user_data["full_name"]
    assert response.json["New user is created"]["email"] == user_from_repo.email == user_data["email"]
    assert response.json["New user is created"]["creation_date"] == user_from_repo.creation_date.isoformat()
    assert pass_hashing.check_password(hashed_password=user_from_repo.password, password=user_data["password"])


def test_create_user_with_integrity_error(test_client, clear_db):
    user_data = {"name": "test_name", "email": "test@email.com", "password": "test_password"}
    manager.create_user(
        user_data=user_data, validate_func=validation.validate_data_for_user_creation,
        hash_pass_func=pass_hashing.hash_password, uow=unit_of_work.UnitOfWork()
    )
    response = test_client.post("http://127.0.0.1:5000/users/", json=user_data)
    assert response.status_code == 409
    assert response.json == {"errors": "A user with the provided params already existsts."}


@pytest.mark.parametrize(
    "user_data,missed_param", (
            ({"name": f"test_name", "password": "test_password"}, "email"),
            ({"email": "email@test.test", "name": f"test_name"}, "password"),
            ({"email": "email@test.test", "password": "test_password"}, "name"),
    )
)
def test_create_user_where_name_or_email_or_password_missed(test_client, user_data, missed_param, clear_db):
    response = test_client.post("http://127.0.0.1:5000/users/", json=user_data)
    assert response.status_code == 400
    assert response.json == {'errors': f"[{{'type': 'missing', 'loc': ('{missed_param}',), 'msg': 'Field required', "
                                       f"'input': {str(user_data)}, "
                                       f"'url': 'https://errors.pydantic.dev/2.10/v/missing'}}]"}


