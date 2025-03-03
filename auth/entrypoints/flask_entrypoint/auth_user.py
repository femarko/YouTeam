from typing import Any
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity

from domain import  custom_errors
from auth.entrypoints import flask_entrypoint
from domain.models import UserColumns


jwt = JWTManager(app=flask_entrypoint.flask_app)


def get_access_token(identity: UserColumns) -> str:
    """
    Creates access token for user authentication, utilizing flask_jwt_extended.create_access_token().

    :param identity: a User model attribute
    :type identity: Any
    :return: access token
    :rtype: str
    """
    return create_access_token(identity=identity)


def get_authenticated_user_identity() -> Any:
    """
    Returns a result of ``flask_jwt_extended.get_jwt_identity()``.

    :return: value of an "identity" parameter, passed to ``flask_jwt_extended.create_access_token()``.
    :rtype: Any
    """
    return get_jwt_identity()


def check_current_user(user_id: int | None = None, get_cuid: bool = True) -> int | None:
    current_user_id: int = get_jwt_identity()
    if user_id is None or user_id == current_user_id:
        if get_cuid is False:
            return
        return current_user_id
    raise custom_errors.CurrentUserError
