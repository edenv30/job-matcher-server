import unittest
from flask import Flask, make_response
from pymongo import MongoClient
from mockupdb import go, OpQuery, MockupDB

def make_app(mongodb_uri):

    app = Flask(__name__)
    db = MongoClient(mongodb_uri)

    @app.route("/pages/<page_name>")
    def page(page_name):
        doc = db.content.pages.find_one({'name': page_name})
        return make_response(doc['contents'])
    # app = Flask(__name__)
    # CORS(app)
    #
    # app.config['MONGODB_DB'] = config.DB_NAME
    # app.config['MONGODB_HOST'] = config.DB_SERVER
    # app.config['MONGODB_PORT'] = config.DB_PORT
    # app.config['MONGODB_USERNAME'] = config.DB_USERNAME
    # app.config['MONGODB_PASSWORD'] = config.DB_PASSWORD
    #
    # app.config['SECRET_KEY'] = config.SECRET_KEY
    #
    # # init database
    # db.init_app(app)
    #
    # # init mail client
    # app.config.update(
    #     DEBUG=True,
    #     MAIL_SERVER=config.MAIL_SERVER,
    #     MAIL_PORT=config.MAIL_PORT,
    #     MAIL_USE_TLS=False,
    #     MAIL_USE_SSL=True,
    #     MAIL_USERNAME=config.MAIL_USERNAME,
    #     MAIL_PASSWORD=config.MAIL_PASSWORD
    # )
    #
    # # init flask rest Api
    # api = Api(app)
    # init_apis(api)
    # dbb = MongoClient(mongodb_uri)
    # @app.route("'/pages/register'")
    # def page(page_name):
    #     doc = dbb.content.pages.find_one({'name': page_name})
    #     return make_response(doc['contents'])
    return app

class MockupDBFlaskTest(unittest.TestCase):
    def setUp(self):
        self.server=MockupDB(3000,'mongodb://localhost')
        self.server.run()
        # print('11111111111',self.server.uri)
        self.app = make_app(self.server.uri).test_client()
        print('000000000',self.app.get)

    def tearDown(self):
        self.server.stop()

    def test(self):
        future = go(self.app.get, "/pages/my_page_name")
        print('11111111',future)
        request = self.server.receives()
        print('22222',request)
        request.reply({"contents": "foo"})
        http_response = future()
        print('333333333',http_response.get_data(as_text=True))
        self.assertEqual("foo",
                         http_response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
