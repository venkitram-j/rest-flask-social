from marshmallow import fields, Schema


class UserSchema(Schema):
    """
    Schema for User
    """

    id = fields.Str(dump_only=True)
    email = fields.Email()
    is_admin = fields.Bool()
    registered_on = fields.Str()
