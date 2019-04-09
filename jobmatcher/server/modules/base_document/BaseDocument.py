import datetime
import mongoengine as me


class BaseDocument(me.Document):
    meta = {'abstract': True}

    create_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    update_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_date = datetime.datetime.now()


# set BaseDocument.pre_save as the function to be called when a user instance was updated
me.signals.pre_save.connect(BaseDocument.pre_save)
