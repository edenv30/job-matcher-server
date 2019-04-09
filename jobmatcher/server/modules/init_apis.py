from jobmatcher.server.authentication.authentication_api import AuthenticationApi
from jobmatcher.server.modules.user.user_api import RegisterUserApi, UserApi
from jobmatcher.server.modules.user.user_api import SignUserApi
from jobmatcher.server.modules.user.user_api import UserUploadApi

def init_apis(api):
    api.add_resource(RegisterUserApi, '/api/users/register')
    api.add_resource(AuthenticationApi, '/api/auth')
    api.add_resource(SignUserApi, '/api/users/signin')
    api.add_resource(UserUploadApi, '/api/user/<string:user_id>/update')


    # api.add_resource(UserCV, '/api/user/<string:user_id>/cv', '/api/user/<string:user_id>/cv/<string:cv_id>')

