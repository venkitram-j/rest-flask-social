"""Business logic for /auth API endpoints."""
from http import HTTPStatus

from flask import current_app, jsonify, views
from flask_smorest import abort, Blueprint

from app import db
from .models import User
from .parameters import (
    UserRegistrationParamter, 
    UserLoginParameter
)


user_blp = Blueprint("Users", __name__)


def _get_token_expire_time():
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds if not current_app.config["TESTING"] else 5

def _create_auth_successful_response(token, status_code, message):
    response = jsonify(
        status="success",
        message=message,
        access_token=token,
        token_type="bearer",
        expires_in=_get_token_expire_time(),
    )
    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response

@user_blp.route("/register")
class RegisterUser(views.MethodView):
    """Handles HTTP requests to URL: /api/v1/auth/register."""

    @user_blp.arguments(UserRegistrationParamter)
    def post(self, request_data):
        """Register a new user and return an access token."""

        email = request_data.get("email")
        password = request_data.get("password")
        admin = request_data.get("admin")

        if User.find_by_email(email):
            abort(HTTPStatus.BAD_REQUEST, status="fail", message=f"{email} is already registered")
        
        new_user = User(email=email, password=password, admin=admin)
        db.session.add(new_user)
        db.session.commit()

        access_token = new_user.encode_access_token()

        return _create_auth_successful_response(
            token=access_token,
            status_code=HTTPStatus.CREATED,
            message="Successfully registered",
        )


@user_blp.route("/login")
class LoginUser(views.MethodView):
    """Handles HTTP requests to URL: /api/v1/auth/login."""

    @user_blp.arguments(UserLoginParameter)
    def post(self, request_data):
        """Authenticate an existing user and return an access token."""

        email = request_data.get("email")
        password = request_data.get("password")

        user = User.find_by_email(email)
        if not user or not user.check_password(password):
            abort(HTTPStatus.UNAUTHORIZED, message="Invalid Credentials", status="fail")
        
        access_token = user.encode_access_token()

        return _create_auth_successful_response(
            token=access_token,
            status_code=HTTPStatus.OK,
            message="Successfully logged in",
        )
