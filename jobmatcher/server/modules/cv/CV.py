import mongoengine as me

from jobmatcher.server.modules.base_document.BaseDocument import BaseDocument


class CV(BaseDocument):
    # defining 'collection' in meta allows us to control the collection name
    meta = {'collection': 'cv'}

    file = me.StringField(required=False)
    text = me.StringField(required=True)
    # tags = me.ListField(me.StringField())

    user = me.ReferenceField('User')

