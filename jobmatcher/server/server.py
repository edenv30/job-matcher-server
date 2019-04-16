import time

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mail import Mail

from jobmatcher.server.db import db
from jobmatcher.server.utils import utils as u
from jobmatcher.config import config
from jobmatcher.server.modules.init_apis import init_apis
from jobmatcher.server.modules.job import scrapUrl

from jobmatcher.server.utils.nltk import nameExtract , skillsExtract ,educationExtract,experienceExtract
from jobmatcher.server.utils.nltk import test

from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
CORS(app)

app.config['MONGODB_DB'] = config.DB_NAME
app.config['MONGODB_HOST'] = config.DB_SERVER
app.config['MONGODB_PORT'] = config.DB_PORT
app.config['MONGODB_USERNAME'] = config.DB_USERNAME
app.config['MONGODB_PASSWORD'] = config.DB_PASSWORD

app.config['SECRET_KEY'] = config.SECRET_KEY

# init database
db.init_app(app)

# init mail client
app.config.update(
    DEBUG=True,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD
)

# init mail client
mail = Mail(app)

# init flask rest Api
api = Api(app)

@app.route('/api/ping')
def ping():
    return 'Pong: %s' % (time.strftime('%c')), u.HTTP_OK


init_apis(api)


def scrape_schedule():
    """
    this function will run in a loop in a set interval
    (defined below inside scheduler.add_job)

    activates scraping function to fetch new jobs information and save it to local DB
    :return:
    """

    # scrapUrl.scarpUrl()
    print('schedule')


# https://apscheduler.readthedocs.io/en/latest/
scheduler = BackgroundScheduler()
# possible interval values:
# https://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html
scheduler.add_job(scrape_schedule, trigger='interval', hours=1)
scheduler.start()

if __name__ == '__main__':
    start_message = 'Job Matcher Server is Running'
    print('@@@@@@@@@@@@@@@@@@@@@@@@')
    print(start_message)
    print('@@@@@@@@@@@@@@@@@@@@@@@@')
    #job_nltk.take_collection()
    # adding new jobs from the web
    #scrapUrl.scarpUrl()

    document_string = " Electronically signed by stupid: Dr. John Douglas, M.D.; Jun 13 2018 11:13AM CST"
    document_string = "John's My name is Eden Varsulker i am study Software engineer and living in Dimona i an student in SCE"

    #nameExtract.extract_name(document_string)
    # skillsExtract.extract_skills('DBA SQL is a leading company in the field of '
    #                              'Internet systems development. '
    #                              'In the role of SQL Server programming versions 2008 and later. '
    #                              'Full time work Sunday through Thursday between 9-18 hours without overtime / '
    #                              'no shifts !! Work in the central region')
    # skillsExtract.extract_skills('B.Sc. in computer science or SW computer engineer  '
    #                              'Experience in OOD / OOP and development in C++ over Linux.Real Time and multitasking programming.'
    #                              'High SW engineering standards')
    # ed = '5+ years as a Product Manager in web/client environment and enterprise B2BExperience with for elegant B.E. 2013'
    # ed2 = ''
    # educationExtract.extract_education()
    experienceExtract.extract_experience(' of experience five years in c++')
    #test.test()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
