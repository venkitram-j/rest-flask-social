"""
Auth extension
"""
from flask import jsonify
from flask_jwt_extended import JWTManager

from app.extensions.flask_sqlalchemy import db
from app.modules.users.models import User, TokenBlocklist


jwt = JWTManager()

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"status": "fail", "message": "The token has expired."}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"status": "fail", "message": "Signature verification failed."}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"status": "fail", "message": "Request does not contain an access token."}), 401

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
    return token is not None

def init_app(app):
    """
    Initialize JWT extension
    """
    
    jwt.init_app(app)
