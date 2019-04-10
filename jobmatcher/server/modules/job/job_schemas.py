import marshmallow_mongoengine as ma

#from jobmatcher.server.modules.job.Job import Job
from.job import Job

class JobSchema(ma.ModelSchema):
    class Meta:
        model = Job

#         test = ma.fields.String()
