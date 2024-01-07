"""Config settings for app
"""
import os


class Config:
    """Base Config
    """

    DEBUG = False
    TESTING = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0

    SQLALCHEMY_DATABASE_URI = "sqlite:///flask_social.db"

    API_TITLE = "Flask Social API Doc"
    API_VERSION = "v1"
    API_ROOT = f"/api/{API_VERSION}"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "jwt": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }

    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


class DevelopmentConfig(Config):
    """Config for development environment
    """

    DEBUG = True

    TOKEN_EXPIRE_MINUTES = 15


class TestingConfig(Config):
    """Config for testing application
    """

    DEBUG = True
    TESTING = True

    JWT_SECRET_KEY = "test-secret"


class ProductionConfig(Config):
    """Config for production environment
    """

    TOKEN_EXPIRE_HOURS = 1


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
