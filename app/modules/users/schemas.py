from marshmallow import fields, Schema


class UserSchema(Schema):
    """Schema for User
    """

    public_id = fields.Str(dump_only=True)
    email = fields.Email()
    admin = fields.Bool()
    registered_on = fields.Str(attribute="registered_on_str")
