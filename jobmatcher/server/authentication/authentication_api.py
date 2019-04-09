from flask import request
from flask_restful import Resource

from jobmatcher.server.authentication.web_token import generate_access_token
from jobmatcher.server.errors import ERRORS
from jobmatcher.server.modules.user.User import User
from jobmatcher.server.utils import utils as u


def wrong_response(payload, error):
    response = {}
    response['success'] = False
    response['errors'] = [ERRORS[error]]
    return response, u.HTTP_UNAUTHORIZED


class AuthenticationApi(Resource):
    def post(self):
        payload = request.json
        response = {}
        try:
            user = User.objects.get(email=payload.get('email').lower())
            if user and user.check_password(payload.get('password')):
                response['success'] = True
                response['token'] = generate_access_token(user).decode('utf-8')
                return response, u.HTTP_OK
            return False, u.HTTP_UNAUTHORIZED
        except User.MultipleObjectsReturned:
            return wrong_response(payload, 'DUPLICATE_USER')
        except User.DoesNotExists:
            return wrong_response(payload, 'EMAIL_OR_PASS_INCORRECT')
