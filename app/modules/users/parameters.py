from marshmallow import fields, Schema, validate


class UserLoginParameter(Schema):
    """
    Parameters for user login request
    """
    
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class UserRegistrationParameter(UserLoginParameter):
    """
    Parameters for user registration request
    """

    is_admin = fields.Bool(load_default=False)
