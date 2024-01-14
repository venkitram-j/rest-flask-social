"""
Flask app initialization via factory pattern.
"""
import os

from flask import Flask

from config import config_map


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_map[os.getenv("APP_ENV", "testing")])

    app.json.sort_keys = False
    
    from . import extensions
    extensions.init_app(app)
    
    from . import modules
    modules.init_app(app)

    return app
