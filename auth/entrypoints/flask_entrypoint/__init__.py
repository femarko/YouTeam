import flask
import os
from dotenv import load_dotenv


load_dotenv()

flask_app = flask.Flask('flask_app')
flask_app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
