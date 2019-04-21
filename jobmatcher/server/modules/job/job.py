import mongoengine as me
import datetime


class Job(me.Document):
    identifier = me.StringField(required=True,unique=True)  # to change this mabye to the link attribute
    role_name = me.StringField(required=True)
    #location = me.ListField(me.StringField(),required=True)
    location = me.StringField(required=True)
    #type = me.ListField(me.StringField(),required=True)
    type = me.StringField(required=True)
    salary = me.StringField()   #default in mongoengine fields are not required
    description = me.StringField(required=True)  # to check mabye to change to list
    requirements = me.StringField(required=True) # to check mabye to change to list
    link = me.StringField()
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_date = datetime.datetime.now()

me.signals.pre_save.connect(Job.pre_save, sender=Job)
