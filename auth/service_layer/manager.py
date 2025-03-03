from datetime import datetime
from typing import Callable, Optional

from domain import custom_errors, services, models


def create_user(
        user_data: dict[str, str], validate_func: Callable, hash_pass_func: Callable, uow
) -> dict[str, str | int]:
    validated_data = validate_func(**user_data)
    validated_data["password"] = hash_pass_func(password=validated_data["password"])
    user = services.create_user(**validated_data)
    with uow:
        uow.users.add(user)
        uow.commit()
        user_id: int = user.id
        created_user_data = services.get_params(model=user)
        return {"id": user_id, **created_user_data}


def jwt_auth(
        validate_func: Callable,
        check_pass_func: Callable[..., bool],
        grant_access_func: Callable,
        credentials: dict[str, str],
        uow
) -> str:
    validated_data = validate_func(**credentials)
    with uow:
        list_of_users: list[models.User] = uow.users.get_by_email(email=validated_data["email"])
    try:
        user: models.User = list_of_users[0]
    except IndexError:
        raise custom_errors.AccessDeniedError
    if check_pass_func(password=validated_data["password"], hashed_password=user.password):
        access_token: str = grant_access_func(identity=user.id)
        return access_token
    raise custom_errors.AccessDeniedError
