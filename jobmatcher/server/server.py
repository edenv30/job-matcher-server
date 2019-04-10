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
    #scrapUrl.scarpUrl()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
