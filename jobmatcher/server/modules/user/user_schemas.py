import marshmallow_mongoengine as ma

from jobmatcher.server.modules.user.User import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

    # test = ma.fields.String()
