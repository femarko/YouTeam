from domain import services, models


def test_create_user():
    user_data = {
        "name": "test_name",
        "email": "test@email.com",
        "password": "test_password"
    }
    user = services.create_user(**user_data)
    assert isinstance(user, models.User)
    assert user.name == "test_name"
    assert user.email == "test@email.com"
    assert user.password == "test_password"
