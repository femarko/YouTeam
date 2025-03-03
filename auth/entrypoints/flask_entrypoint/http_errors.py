import flask

from auth.entrypoints.flask_entrypoint import flask_app


class HttpError(Exception):
    def __init__(self, status_code: int, description: str | list | set):
        self.status_code = status_code
        self.description = description


@flask_app.errorhandler(HttpError)
def error_handler(error):
    response = flask.jsonify({"errors": error.description})
    response.status_code = error.status_code
    return response
