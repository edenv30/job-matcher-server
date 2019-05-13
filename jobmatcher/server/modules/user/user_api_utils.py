from flask import request
from flask_restful import Resource

from jobmatcher.server.modules.user.User import User

from jobmatcher.server.utils.nltk.extract_details import extract_location
from jobmatcher.server.utils.word2vec.matching import match_jobs2cv, get_list_matching_job

def checkUserFile(user_id):
    # print("checkUserFile")
    # print("user_id: ")
    # print(user_id)
    user = User.objects.get(pk=user_id)
    if user.cvs == None:
        return True
    return False

def findMatchWord2vec(user_id):
    print('~~~~~ func findMatchWord2vec from user_api_utils ~~~~~')
    user = User.objects.get(pk=user_id)
    # if len(user.cvs) == 0:
    #     # print('len(user.cvs)', len(user.cvs))
    #     return None
    cv_id = user.cvs[0].id
    cv_text = user.cvs[0].text
    # for location score
    user_location = []
    user_location = extract_location(cv_text)
    jobs_id_list = match_jobs2cv(cv_text, user_location)
    for k, v in jobs_id_list.items():
        if k not in user.jobs:
            user.favorite[k] = False
            user.sending[k] = False
            user.replay[k] = False
            user.jobs[k] = v
    user.save()
    # response = get_list_matching_job(jobs_id_list, user_id)
    # print(response)
    # return response