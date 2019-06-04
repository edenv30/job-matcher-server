from flask_restful import Resource
from flask import request
from mongoengine import NotUniqueError
from mongoengine import connect

#from jobmatcher.server.modules.job.Job import Job
# from jobmatcher.config import config
from.job import Job
from jobmatcher.server.utils import utils as u

# from pymongo import MongoClient  # to connect the data base

class UploadJobApi(Resource):
    def get(self):
        print('~~~~~ In func GET in UploadJobApi ~~~~~')
        '''
        for job in Job.objects:
            print(job.identifier)
            print(job.role_name)
        '''
        response = [{} for i in range(Job.objects.__len__())]
        i = 0
        for job in Job.objects:
            response[i]["identifier"] = job.identifier
            response[i]["role_name"] = job.role_name
            response[i]["location"] = job.location
            response[i]["type"] = job.type
            response[i]["salary"] = job.salary
            response[i]["description"] = job.description
            response[i]["requirements"] = job.requirements
            response[i]["link"] = job.link
            i += 1
        return response, u.HTTP_CREATED

        '''
        client = MongoClient(config.DB_SERVER, config.DB_PORT)
        db_for_job = cl

ient[config.DB_NAME]
        collection_job = db_for_job[config.COLLECTION_JOB]
        cursor = collection_job.find()

        for doc in cursor:
            if doc["id"]== id:
                print (doc)

        for doc in cursor:
            print('-----------------')
            #print(doc["id"])
            print(doc)

                client.close()
        return cursor,u.HTTP_CREATED
        '''

class jobsCounter(Resource):
    def get(self):
        # print('~~~~~ In func GET in jobsCounter ~~~~~')
        return len(Job.objects)