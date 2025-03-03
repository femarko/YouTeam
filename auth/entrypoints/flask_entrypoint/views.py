import flask

import domain.custom_errors
from auth.entrypoints.flask_entrypoint import flask_app, http_errors
from auth.service_layer import manager
from auth.service_layer.unit_of_work import UnitOfWork
from auth.validation_and_pass_hashing import validation, pass_hashing


@flask_app.route("/users/", methods=["POST"])
def create_user():
    try:
        new_user_data: dict[str, str | int] = manager.create_user(
            user_data=flask.request.json, validate_func=validation.validate_data_for_user_creation,
            hash_pass_func=pass_hashing.hash_password, uow=UnitOfWork()
        )
    except domain.custom_errors.ValidationError as e:
        raise http_errors.HttpError(status_code=400, description=str(e))
    except domain.custom_errors.AlreadyExistsError as e:
        raise http_errors.HttpError(status_code=409, description=f"A user {e.message}")
    except domain.custom_errors.InternalServerError as e:
        raise http_errors.HttpError(status_code=500, description=e.message)
    return flask.jsonify({"New user is created": new_user_data}), 201
