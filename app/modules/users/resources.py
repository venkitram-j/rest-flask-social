"""
User/Authentication endpoints
"""
from flask import request, current_app
from flask.views import MethodView
from flask_smorest import abort, Page
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity
)

from app.extensions.api import CustomBlueprint
from .models import User, TokenBlocklist
from .parameters import (
    UserRegistrationParameter, 
    UserLoginParameter
)
from .schemas import UserSchema


blp = CustomBlueprint("Users", __name__)


@blp.route("/")
class Users(MethodView):
    
    @blp.doc(security=[{"jwt": []}])
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    @blp.paginate()
    def get(self):
        """
        Get list of paginated users
        """
        
        page = request.args.get("page", default=1, type=int)
        page_size = request.args.get("page_size", default=current_app.config["DEFAULT_PAGE_SIZE"], type=int)
        
        claims = get_jwt()
        
        if claims.get("is_admin"):
            return User.query.paginate(page=page, per_page=page_size)
        
        return User.query.filter_by(is_admin=False).paginate(page=page, per_page=page_size)
        

@blp.route("/register")
class RegisterUser(MethodView):

    @blp.arguments(UserRegistrationParameter)
    def post(self, request_data):
        """
        Create a new user
        """

        user = User.get_user_by_email(email=request_data.get("email"))
        
        if user is not None:
            abort(409, message="A user with that email already exists!!")

        new_user = User(
            email=request_data["email"],
            first_name=request_data["first_name"],
            last_name=request_data["last_name"],
            is_admin=request_data["is_admin"]
        )
        new_user.set_password(password=request_data["password"])
        new_user.save()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class LoginUser(MethodView):

    @blp.arguments(UserLoginParameter)
    def post(self, request_data):
        """
        Authenticate an existing user and return an access token.
        """

        user = User.get_user_by_email(email=request_data.get("email"))

        if user and user.check_password(password=request_data["password"]):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.get("/refresh")
class RefreshToken(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        """
        Accept a refresh token to generate a new access token
        """
        
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        
        return {"access_token": new_access_token}, 200


@blp.route("/logout")
class LogoutView(MethodView):
    
    @blp.doc(security=[{"jwt": []}])
    @jwt_required(verify_type=False)
    def post(self):
        """
        User logout
        """
        
        jwt = get_jwt()["jti"]
        token = TokenBlocklist(jti=jwt)
        token_type = jwt["type"]
        token.save()

        return {"message": f"{token_type} token revoked successfully."}, 200
