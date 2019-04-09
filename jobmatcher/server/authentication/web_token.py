import jwt, time

# 60 days of TTL
from jobmatcher.config import config

TTL_DAYS = 60
ACCESS_TOKEN_TTL = 24 * 60 * 60 * TTL_DAYS


def generate_access_token(db_user):
    user = {
        'id': str(db_user.id),
        'first_name': db_user.first_name,
        'last_name': db_user.last_name,
        'fullname': db_user.fullname,
        'tags': db_user.tags,
    }

    return jwt.encode({
        'user': user,
        'timestamp': time.time()
    }, config.SECRET_KEY)


def get_user_from_access_token(access_token):
    try:
        decoded_token = jwt.decode(access_token, config.SECRET_KEY)
        if time.time() - decoded_token.get('timestamp') < ACCESS_TOKEN_TTL:
            return decoded_token.get('user')
    except Exception as e:
        pass
    return None
