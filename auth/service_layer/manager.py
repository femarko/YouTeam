from datetime import datetime
from typing import Callable, Optional

from domain import custom_errors, services, models


def create_user(user_data: dict[str, str], validate_func: Callable, hash_pass_func: Callable, uow):
    validated_data = validate_func(**user_data)
    validated_data["password"] = hash_pass_func(password=validated_data["password"])
    user = services.create_user(**validated_data)
    with uow:
        uow.users.add(user)
        uow.commit()
        user_id: int = user.id
        return user_id
