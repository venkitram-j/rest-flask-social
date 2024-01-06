"""Flask app initialization via factory pattern.
"""
import os

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import config_map


api = Api()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_map[os.getenv("APP_ENV", "testing")])

    api.init_app(app)
    jwt.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    return app

