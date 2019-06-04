from jobmatcher.server.authentication.authentication_api import AuthenticationApi
from jobmatcher.server.modules.user.user_api import RegisterUserApi,UserUpdateApi,UserSetStusApi
from jobmatcher.server.modules.user.user_api import SignUserApi
from jobmatcher.server.modules.user.user_api import UserUploadApi
from jobmatcher.server.modules.job.job_api import UploadJobApi,jobsCounter
from jobmatcher.server.modules.user.user_api import UserPreferencesApi
from jobmatcher.server.modules.user.user_api import UserFindMatchApi
from jobmatcher.server.modules.user.user_api import UserFindMatchWord2vecApi,UserFindMatchWord2vecApi2
from jobmatcher.server.modules.user.user_api import UserGetRecommendation
from jobmatcher.server.modules.user.user_api import jobsSortBYscore,UpdateSending,PDFfile
from jobmatcher.server.modules.user.user_api import jobsSortBYlocation,UpdateFavorite,UpdateReply
from jobmatcher.server.modules.user.user_api import UserTimeLine,RegistersUserCounter,UsersFindJobCounter
from jobmatcher.server.modules.user.user_api import UserContact


def init_apis(api):
    api.add_resource(RegisterUserApi, '/api/users/register')
    api.add_resource(UserUpdateApi, '/api/user/<string:user_id>/changeProfile')
    api.add_resource(UserSetStusApi, '/api/user/<string:user_id>/set_status')
    api.add_resource(AuthenticationApi, '/api/auth')
    api.add_resource(SignUserApi, '/api/users/signin')
    api.add_resource(UserUploadApi, '/api/user/<string:user_id>/update')
    api.add_resource(UploadJobApi, '/api/jobs/upload')
    api.add_resource(UserPreferencesApi, '/api/user/<string:user_id>/preferences')
    # api.add_resource(UserFindMatchApi, '/api/user/<string:user_id>/svemtchjbs')
    api.add_resource(UserFindMatchWord2vecApi, '/api/user/<string:user_id>/word2vec')
    api.add_resource(UserFindMatchWord2vecApi2, '/api/user/<string:user_id>/word2vec2')
    api.add_resource(UserGetRecommendation, '/api/user/<string:user_id>/recommendation')
    api.add_resource(jobsCounter,'/api/jobscounter')
    api.add_resource(RegistersUserCounter,'/api/registersusercounter')
    api.add_resource(UsersFindJobCounter,'/api/usersfindjobcounter')
    api.add_resource(jobsSortBYscore,'/api/user/<string:user_id>/sortBYscore')
    api.add_resource(jobsSortBYlocation,'/api/user/<string:user_id>/sortBYlocation')
    api.add_resource(UpdateFavorite,'/api/user/<string:user_id>/UpdateFavorite')
    api.add_resource(UpdateSending, '/api/user/<string:user_id>/UpdateSending')
    api.add_resource(UpdateReply, '/api/user/<string:user_id>/UpdateReply')
    api.add_resource(UserTimeLine, '/api/user/<string:user_id>/UserTimeLine')
    api.add_resource(PDFfile, '/api/user/<string:user_id>/PDFfile')
    api.add_resource(UserContact, '/api/users/contact')


