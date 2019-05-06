from flask_restful import Resource
from flask import request, session
from mongoengine import NotUniqueError
import json

from mongoengine import connect

from jobmatcher.server.authentication.authentication import require_authentication
from jobmatcher.server.authentication.web_token import generate_access_token
from jobmatcher.server.modules.user.user_schemas import UserSchema
from jobmatcher.server.utils import utils as u

from jobmatcher.server.modules.user.User import User
from jobmatcher.server.modules.cv.CV import CV
from jobmatcher.server.modules.job.job import Job

# import all nltk - extract fields functions
from jobmatcher.server.utils.nltk.extract_details import extract_education
from jobmatcher.server.utils.nltk.extract_details import extract_experience
from jobmatcher.server.utils.nltk.extract_details import extract_skills
from jobmatcher.server.utils.nltk.extract_details import extract_location
from jobmatcher.server.utils.word2vec.matching import match_jobs2cv,get_list_matching_job
from jobmatcher.server.utils.location.location import matchHandler , one_city

from jobmatcher.server.modules.user.user_api_utils import checkUserFile
from jobmatcher.server.utils.dict_lang_programing import recommendation
# from jobmatcher.server.utils.location.location import handle_location_match
from jobmatcher.server.utils.location.location import matchHandler


class RegisterUserApi(Resource):
    def post(self):
        payload = request.json.get('body')

        try:
            user = User(
                first_name=payload.get('first_name'),
                last_name=payload.get('last_name'),
                email=payload.get('email').lower(),
                active=True,
                tags=payload.get('tags')
            )
            user.set_password(payload.get('password'))
            user.save()
        except NotUniqueError as e:
            return {'errors': ['Email address already in use']}, u.HTTP_BAD_INPUT

        # user_schema = UserSchema(exclude=['password_hash'])
        # response = user_schema.dump(user).data
        response = {}
        response['success'] = True
        response['token'] = generate_access_token(user).decode('utf-8')
        return response, u.HTTP_CREATED


class SignUserApi(Resource):
    def post(self):
        payload = request.json
        user = User.objects.get(email=payload.get('email', None))
        print("SUCCESS!!!!!!!!!")
        # userEmail = User.objects(email="test@email.com")
        #         # print(userEmail)

        for user in User.objects.get(email="test@email.com"):
            print(user.email)
            self.find_by_email("test@email.com")


class UserApi(Resource):
    @require_authentication
    def put(self, user_id):
        """
        edits a user profile
        :return:
        """
        payload = request.json


class UserUploadApi(Resource):
    @require_authentication
    def post(self, user_id):
        try:
            # check that the given user_id matches the logged in user id
            assert user_id == session['user']['id']
        except AssertionError:
            return {'errors': ['You are Unauthorized in this EP']}, u.HTTP_UNAUTHORIZED

        payload = request.json

        # if not (checkUserFile(user_id)):
        #     print("User cannot upload file !!!!!!!!!!!!!!!!!!")
        #     return False



        # get the user instance from the users collection
        user = User.objects.get(pk=user_id)
        cv = CV(
            text=payload.get('data'),
            user=user.to_dbref()
        )
        cv.save()
        # add the CV DBRef to the user cvs list
        user.cvs.append(cv.to_dbref())
        user.save()
        return {}, u.HTTP_CREATED

class UserUpdateApi(Resource):

    def post(self, user_id):
        print('------ post update profile ------')
        payload = request.json.get('body')
        # print(payload)
        user = User(
            first_name=payload.get('first_name'),
            last_name=payload.get('last_name'),
            email=payload.get('email').lower(),
            active=True,
            tags=payload.get('tags')
        )
        user.set_password(payload.get('password'))
        ppost = User.objects.get(email=payload.get('email', None))
        ppost.first_name=user.first_name
        ppost.last_name = user.last_name
        ppost.password_hash = user.password_hash
        ppost.active = user.active
        ppost.tags=user.tags
        print(ppost.tags)
        ppost.save()

    def get (self,user_id):
        # print('------ get update profile ------')
        # print(user_id)
        user=User.objects.get(id=user_id)
        # print (user.first_name)
        # print("user_tags_amount")
        # print(len(user.tags))
        return [user.first_name,user.last_name,user.email,len(user.tags),user.tags,user.password_hash]

class UserSetStusApi(Resource):
    def get (self,user_id):
        print('------ get state status ------')
        # print(user_id)
        user=User.objects.get(id=user_id)
        user.find=False
        user.save()
        # print (user.first_name)
        return [user.find]

class UserPreferencesApi(Resource):
    @require_authentication
    def post(self, user_id):
        # TODO: adding assert, adding try&except,user will be able to load only 1 CV file
        # TODO: taking care if user want to delete his current cv file, change method to PUT(instead of POST)
        print("UserPreferencesApi")
        print(user_id)
        payload = request.json.get('body')
        kind = payload.get('type')
        print(kind)

        user = User.objects.get(pk=user_id)
        print("#### " + user.email)
        user.job_type = kind
        print(user.job_type)
        user.save()


class UserFindMatchApi(Resource):
    @require_authentication
    def post(self, user_id):
        # print(" === UserFindMatchApi ===")
        # print("user_id: " + user_id)

        user = User.objects.get(pk=user_id)
        resume = user.cvs[0].text

        user_location = []
        user_location = extract_location(resume)
        # TODO: change
        job = Job.objects.first()  # getting job id for the first object - temp for now
        job_id = job.id
        matchHandler(job_id, user_location)

class UserFindMatchWord2vecApi(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ UserFindMatchWord2vecApi ~~~~~')
        # TODO: בשלב הסופי כשהכל תקין - להחזיר את ההערות ולמחוק את הפרטים הסטטיים
        user = User.objects.get(pk=user_id)
        cv_id = user.cvs[0].id
        cv_text = user.cvs[0].text
        # for location score
        # user_location = []
        # user_location = extract_location(cv_text)
        # jobs_id_list = match_jobs2cv(cv_text,user_location)
        # for k,v in jobs_id_list.items():
        #     if k not in  user.jobs:
        #         user.jobs[k] = v
        # user.save()
        # response = get_list_matching_job(jobs_id_list)
        # # print(response)
        # return response
        response = {123: ('example', 'https://www.jobmaster.co.il/jobs/?headcatnum=15&lang=en',0.8,True,False),
                    234: ('Client-side developer','https://www.jobmaster.co.il/jobs/?headcatnum=15&lang=en',0.9,False,True),
                    222: ('e', 'd',0.7,True,True), 111: ('eee','qweqwee',0.8,False,True),333:('e','e',0.8,True,False), 1212: ('w','w',0.8,True,True),
                    1234: ('w', 'w', 0.8, True, True),1762: ('w','w',0.8,True,True),
                    444: ('e', 'd', 0.7,False,False), 555: ('eee', 'qweqwee', 0.8,False,True), 666: ('e', 'e', 0.8,True,False), 777: ('wewe', 'w', 0.8,False,False),
                    888:('dba man','link',0.9), 999: ('sql man','link',0.9), 1515: ('client side','link', 0.78),
                    3434:('server','link',0.87)}
        return response


class UserGetRecommendation(Resource):
    @require_authentication
    def post(self, user_id):
        print("UserGetRecommendation")
        rec = {}
        rec = recommendation(user_id)
        print("rec:")
        print(rec)

import operator

# x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
# sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
# print(sorted_x)

class jobsSortBYscore(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ jobsSortBYscore ~~~~~')
        user = User.objects.get(pk=user_id)

        jobs_user = user.jobs

        # sorted(jobs_user.values(), reverse=True)
        # score_list = sorted(["{:.3f}".format(v) for k,v in jobs_user.items()],reverse=True)
        # print(score_list)

        sorted_score = sorted(jobs_user.items(), key=operator.itemgetter(1), reverse=True)
        # print(sorted_score)

        response = {}
        for t in sorted_score:
            # job = t[0]
            job = Job.objects.get(identifier=t[0])
            response[t[0]] = (job.role_name, job.link,t[1])

        # print(response)
        return response

class jobsSortBYlocation(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ jobsSortBYlocation ~~~~~')
        user = User.objects.get(pk=user_id)
        cv_text = user.cvs[0].text
        # TODO: לבדוק האם זה משנה אם הפונקציה שמוצאת עיר אחת לא נופלת אם למשתמש יש רשימת ערים של יותר מעיר אחת
        user_location = []
        user_location = extract_location(cv_text)
        loc_dict = {}
        jobs_user = user.jobs
        # to keep the lication of job in dictionary
        for k,v in jobs_user.items():
            job = Job.objects.get(identifier=k)
            city = one_city(k, user_location)
            loc_dict[k] = city
        #sort list of tuples (job_id,city) by order alphabet cities
        sorted_loc = sorted(loc_dict.items(), key=operator.itemgetter(1))
        response = {}
        for s in sorted_loc:
            job = Job.objects.get(identifier=s[0])
            response[s[0]] = (job.role_name,job.link,v,s[1])
        # print(response)
        return response



