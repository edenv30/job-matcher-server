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
    skillsExtract.extract_skills('Sr. Specialist, IT Administration'
                                 'T-Mobile USA beer sheeva!, USA'
                                 'T-Mobile USA Inc is the third largest Telecommunications company in the United States that '
                                 'employees over 51,000 across the arad. I live in tel-aviv retail environment.'
                                 'Supported 15 plus retail stores with their computer equipment issues. Remotely or traveled to site. Throughout my tenure at T-Mobile I was always getting customer and team recognition for achievements and excellent service. Some of the projects I have worked on...')
    # skillsExtract.extract_skills('B.Sc. in computer science or SW computer engineer  '
    #                              'Experience in OOD / OOP and development in C++ over Linux.Real Time and multitasking programming.'
    #                              'High SW engineering standards')
    # ed = '5+ years as a Product Manager in web/client environment and enterprise B2BExperience with for elegant B.E. 2013'
    # ed2 = ''
    # educationExtract.extract_education()
    #experienceExtract.extract_experience(' of experience five years in c++')
    #test.test()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
