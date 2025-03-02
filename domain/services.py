from domain.models import User


def create_user(**user_data) -> User:
    return User(**user_data)


def get_params(model: User) -> dict[str, str | int]:
    if isinstance(model, User):
        return {
            "id": model.id, "name": model.name, "email": model.email, "creation_date": model.creation_date.isoformat()
        }
    return dict()
