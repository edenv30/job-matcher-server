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

    # def find_by_email(self, email):
    #     connect('job_matcher', port=27017)
    #     print("_find_by_email_function")
    #     result = list(User.objects(email= email))
    #     print(result[0].first_name)
    #     result[0].password_hash
    #     convertPassword = check_password(result[0].password_hash)

    # /users
    # /user/76776 =====> PUT

    def post(self):
        # connect('job_matcher', port=27017)
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
        print('------ get update profile ------')
        # print(user_id)
        user=User.objects.get(id=user_id)
        # print (user.first_name)
        return [user.first_name,user.last_name,user.email,user.tags,user.password_hash]