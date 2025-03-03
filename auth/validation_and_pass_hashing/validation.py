import pydantic
from typing import TypeVar, Type, Optional

from domain import custom_errors


PydanticModel = TypeVar("PydanticModel", bound=pydantic.BaseModel)


class CreateUser(pydantic.BaseModel):
    name: str
    full_name: Optional[str] = None
    email: str
    password: str


class Login(pydantic.BaseModel):
    email: str
    password: str


def validate_data(validation_model: Type[PydanticModel], data: dict[str, str]):
    try:
        return validation_model.model_validate(data).model_dump(exclude_unset=True)
    except pydantic.ValidationError as e:
        raise custom_errors.ValidationError(e.errors())


def validate_login_credentials(**credentials):
    return validate_data(validation_model=Login, data={**credentials})


def validate_data_for_user_creation(**user_data):
    return validate_data(validation_model=CreateUser, data={**user_data})
