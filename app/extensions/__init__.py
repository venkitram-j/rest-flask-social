"""
Initialize extensions
"""
from . import api, auth, flask_sqlalchemy

def init_app(app):
    
    api.init_app(app)
    auth.init_app(app)
    flask_sqlalchemy.init_app(app)
