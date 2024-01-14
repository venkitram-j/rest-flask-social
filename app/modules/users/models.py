"""User models."""
import uuid
import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions.flask_sqlalchemy import db


class User(db.Model):
    """
    Model for storing user details
    """

    __tablename__ = "user"

    id = db.Column(db.String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """
        The __repr__ function is used to return a string representation of the object
        """
        return (
            f"<User email={self.email}, admin={self.admin}>"
        )
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
class TokenBlocklist(db.Model):
    """
    Model for storing tokens invalidated 
    during logout
    """
    
    __tablename__ = "token_blocklist"
    
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=True)
    create_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
