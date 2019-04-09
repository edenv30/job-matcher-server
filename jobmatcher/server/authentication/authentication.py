from functools import wraps

from flask import session, request

from jobmatcher.server.authentication.web_token import get_user_from_access_token
from jobmatcher.server.modules.user.User import User
from jobmatcher.server.utils import utils as u


def extract_user_from_access_token(access_token):
    user = get_user_from_access_token(access_token)
    if user:
        try:
            db_user = User.objects.get(pk=user.get('id'))
        except User.DoesNotExist:
            return False
        if db_user and db_user.active is True:
            session['user'] = user
            return True
    return False


def require_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if not access_token or not extract_user_from_access_token(access_token):
            return 'You need to authenticate!', u.HTTP_UNAUTHORIZED
        return f(*args, **kwargs)

    return decorated
