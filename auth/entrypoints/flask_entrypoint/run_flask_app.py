from orm import table_mapper
from auth.entrypoints.flask_entrypoint import flask_app


if __name__ == "__main__":
    table_mapper.start_mapping()
    flask_app.run(debug=True)
