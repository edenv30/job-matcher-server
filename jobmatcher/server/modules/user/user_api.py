from flask_restful import Resource
from flask import request, session
from mongoengine import NotUniqueError
from jobmatcher.server.authentication.authentication import require_authentication
from jobmatcher.server.authentication.web_token import generate_access_token
from jobmatcher.server.utils import utils as u
from jobmatcher.server.modules.user.User import User
from jobmatcher.server.modules.cv.CV import CV
from jobmatcher.server.modules.job.job import Job
from jobmatcher.server.utils.nltk.extract_details import extract_location,extract_type
from jobmatcher.server.utils.location.location import one_city
from jobmatcher.server.utils.dict_lang_programing import recommendation
from jobmatcher.server.utils.location.location import matchHandler
from jobmatcher.server.utils.SOS import pdfFIle
from jobmatcher.server.utils.word2vec.matching import match_jobs2cv,get_list_matching_job
from jobmatcher.server.modules.user.user_api_utils import findMatchWord2vec
import operator, datetime


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
        if(ppost.password_hash!=payload.get('password')):
            ppost.password_hash = user.password_hash
        ppost.active = user.active
        ppost.tags=user.tags
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
    def get(self,user_id):
        user = User.objects.get(pk=user_id)
        return [user.job_type]

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
        if len(user.cvs) == 0:
            # print('len(user.cvs)')
            return None
        cv_id = user.cvs[0].id
        cv_text = user.cvs[0].text
        #for location score
        user_location = []
        user_location = extract_location(cv_text)
        jobs_id_list = match_jobs2cv(cv_text,user_location)
        for k,v in jobs_id_list.items():
            if k not in user.jobs:
                user.favorite[k]=False
                user.sending[k]=False
                user.replay[k]=False
                user.jobs[k] = v
        user.save()
        response = get_list_matching_job(jobs_id_list,user_id)
        # print(response)
        return response


        # # # #TODO: לקטע קוד האמיתי זה ההערות הראשונות
        # response={}
        # jobs = user.jobs
        #
        # for k ,v in jobs.items():
        #     job = Job.objects.get(identifier=k)
        #     response[k]=(job.role_name,job.link,v,extract_type(job.type),
        #                  user.favorite[k],user.sending[k],user.replay[k])
        # print(response)
        # return response

class UserFindMatchWord2vecApi2(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ UserFindMatchWord2vecApi ~~~~~')
        # TODO: בשלב הסופי כשהכל תקין - להחזיר את ההערות ולמחוק את הפרטים הסטטיים
        user = User.objects.get(pk=user_id)
        if len(user.cvs) == 0:
            # print('len(user.cvs)')
            return None
        # cv_id = user.cvs[0].id
        # cv_text = user.cvs[0].text
        # #for location score
        # user_location = []
        # user_location = extract_location(cv_text)
        # jobs_id_list = match_jobs2cv(cv_text,user_location)
        # for k,v in jobs_id_list.items():
        #     if k not in user.jobs:
        #         user.favorite[k]=False
        #         user.sending[k]=False
        #         user.replay[k]=False
        #         user.jobs[k] = v
        # user.save()
        # response = get_list_matching_job(jobs_id_list,user_id)
        # print(response)
        # return response


        # # # #TODO: לקטע קוד האמיתי זה ההערות הראשונות
        response={}
        jobs = user.jobs

        for k ,v in jobs.items():
            job = Job.objects.get(identifier=k)
            response[k]=(job.role_name,job.link,v,extract_type(job.type),
                         user.favorite[k],user.sending[k],user.replay[k])
        # print(response)
        return response

class UserGetRecommendation(Resource):
    @require_authentication
    def post(self, user_id):
        print("UserGetRecommendation")
        # rec = []
        rec = recommendation(user_id)
        # print("rec:")
        # print(rec)

        return rec

class jobsSortBYscore(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ jobsSortBYscore ~~~~~')
        user = User.objects.get(pk=user_id)
        if len(user.cvs)==0:
            # print('len(user.cvs)', len(user.cvs))
            return None
        # findMatchWord2vec(user_id)
        # sorted(jobs_user.values(), reverse=True)
        # score_list = sorted(["{:.3f}".format(v) for k,v in jobs_user.items()],reverse=True)
        jobs_user = user.jobs
        # print('jobs_user: ', jobs_user)
        sorted_score = sorted(jobs_user.items(), key=operator.itemgetter(1), reverse=True)
        # print('sorted_score: ',sorted_score)

        response = {}
        for t in sorted_score:
            # job = t[0]
            job = Job.objects.get(identifier=t[0])
            response[t[0]] = (job.role_name, job.link,t[1],user.favorite[t[0]],user.sending[t[0]]
                              ,user.replay[t[0]])

        print(response)
        return response

class jobsSortBYlocation(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ jobsSortBYlocation ~~~~~')
        user = User.objects.get(pk=user_id)
        if len(user.cvs)==0:
            return None
        # findMatchWord2vec(user_id)
        cv_text = user.cvs[0].text
        # TODO: לבדוק האם זה משנה אם הפונקציה שמוצאת עיר אחת לא נופלת אם למשתמש יש רשימת ערים של יותר מעיר אחת
        user_location = extract_location(cv_text)
        loc_dict = {}
        jobs_user = user.jobs
        # print('jobs_user: ', jobs_user)
        # to keep the location of job in dictionary
        for k,v in jobs_user.items():
            # job = Job.objects.get(identifier=k)
            city = one_city(k, user_location)
            loc_dict[k] = city
        #sort list of tuples (job_id,city) by order alphabet citie
        sorted_loc = sorted(loc_dict.items(), key=operator.itemgetter(1))
        # print('sorted_loc: ', sorted_loc)
        response = {}
        for s in sorted_loc:
            score = 0
            for k,v in jobs_user.items():
                if (s[0]==k):
                    score = v
                    break
            job = Job.objects.get(identifier=s[0])
            response[s[0]] = (job.role_name,job.link,score,s[1],user.favorite[s[0]],user.sending[s[0]]
                              ,user.replay[s[0]])
        # print(response)
        return response

class UpdateFavorite(Resource):
    @require_authentication
    def post(self, user_id):
        print('------ post test ------')
        payload = request.json.get('body')
        job_id=payload.get('id')
        user = User.objects.get(id=user_id)
        if(user.favorite[job_id]==False):
            user.favorite[job_id]=True
        else:
            user.favorite[job_id]=False
        user.save()

class UpdateSending(Resource):
    @require_authentication
    def post(self, user_id):
        print('------ post test ------')
        payload = request.json.get('body')
        job_id=payload.get('id')
        user = User.objects.get(id=user_id)
        if(user.sending[job_id]==False):
            user.sending[job_id]=True
            # user.sendingDate[job_id]=datetime.datetime.now()
            user.sendingDate[job_id] = datetime.datetime.today()
        else:
            user.sending[job_id]=False
            if job_id in user.sendingDate:
                user.sendingDate.pop(job_id, None)
        user.save()

class UpdateReply(Resource):
    @require_authentication
    def post(self, user_id):
        payload = request.json.get('body')
        job_id = payload.get('id')
        user = User.objects.get(id=user_id)
        if (user.replay[job_id] == False):
            user.replay[job_id] = True
            user.replyDate[job_id] = datetime.datetime.today()
        else:
            user.replay[job_id] = False
            if job_id in user.replyDate:
                user.replyDate.pop(job_id, None)
        user.save()

class UserTimeLine(Resource):
    @require_authentication
    def post(self, user_id):
        print('~~~~~ UserTimeLine ~~~~~')
        user = User.objects.get(id=user_id)
        response = {}
        dates ={}
        #  keep in dictionary key by date from sending dictionary
        for job in user.sendingDate:
            d = user.sendingDate[job].strftime("%d/%m/%Y")
            dic = {}
            if d not in dates:
                dates[d] = []
            # TODO: לעשות בדיקה אם אין משרות , תנאי
            j = Job.objects.get(identifier=job)
            dic[job]=j.role_name, 'SENT: CVs were sent to the employer'
            dates[d].append(dic)
        #  keep in dictionary key by date from reply dictionary
        for job in user.replyDate:
            d = user.replyDate[job].strftime("%d/%m/%Y")
            dic = {}
            j = Job.objects.get(identifier=job)
            dic[job]=j.role_name,'REPLY: An employer came back'
            if d not in dates:
                dates[d] = []
            dates[d].append(dic)
        # to order by most new updated and return only 3 dates
        i=0
        for date in reversed(sorted(dates.keys())):
            i+=1
            response[date] = dates[date]
            if i==3:
                break;

        # print(response)
        return response

class PDFfile(Resource):
    def post(self,user_id):
        print('------PDFfile----')
        payload = request.json.get('body')
        url=payload.get('urlFile')
        user = User.objects.get(id=user_id)
        # receiver=user.email
        receiver='chenyair1617@gmail.com'
        subject= 'This is the subject'
        message='This is the message'
        print(url)
        # print('user',user.email)
        pdfFIle.convertHtmlToDfdFile(url,receiver,subject,message)