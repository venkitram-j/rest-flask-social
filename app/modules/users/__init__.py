"""
Users module initialisation
"""
from app.extensions.api import api

def init_app(app):
    from . import models, resources
    
    api.register_blueprint(
        resources.blp, 
        url_prefix=f"{app.config['API_ROOT']}/users"
    )
