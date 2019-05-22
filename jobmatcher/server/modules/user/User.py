import mongoengine as me

from jobmatcher.server.modules.base_document.BaseDocument import BaseDocument
# import CV so it will be recognized in => me.ListField(me.ReferenceField('CV'))
from jobmatcher.server.modules.cv.CV import CV

from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseDocument):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    email = me.StringField(unique=True, required=True)
    password_hash = me.StringField(required=True)
    job_type = me.StringField(required=True,default='none')
    active = me.BooleanField(required=True, default=True)

    tags = me.ListField(me.StringField())

    # cvs = me.ListField(me.ReferenceField('CV'))
    cvs = me.ListField(me.ReferenceField('CV', reverse_delete_rule=me.PULL))

    #matches = me.ListField(me.ReferenceField('JOB'))

    jobs = me.DictField(required=False)
    favorite = me.DictField(required=False)
    sending = me.DictField(required=False)
    replay = me.DictField(required=False)
    find = me.BooleanField(required=False)
    sendingDate = me.DictField(required=False)
    replyDate = me.DictField(required=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def fullname(self):
        return '%s %s' % (self.first_name, self.last_name)
