from marshmallow import fields, Schema


class UserLoginParameter(Schema):
    """Parameters for user login request
    """
    
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserRegistrationParamter(UserLoginParameter):
    """Parameters for user registration request
    """

    admin = fields.Bool(load_default=False)
