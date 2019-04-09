import marshmallow_mongoengine as ma

from jobmatcher.server.modules.cv.CV import CV


class CVSchema(ma.ModelSchema):
    class Meta:
        model = CV

    # test = ma.fields.String()
