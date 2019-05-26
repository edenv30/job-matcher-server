# import unittest
# import requests
# from bs4 import BeautifulSoup
# from unittest.mock import Mock
#
# class TestBasicFunction(unittest.TestCase):
#     def test(self):
#         self.assertTrue(True)
#
#     def test_request_response(self):
#         # url = 'http://localhost:{port}'.format(port=3000)
#         # url = 'http://localhost:3000.html'
#         # url = 'localhost:3000.html'
#         # url = 'https://python-forum.io/Thread-An-Error-in-Requests-Module'
#         # url = 'https://python-forum.io/Thread-Error-in-Requests-Module'
#         d = {'email': 'edenva@ac.sce.ac.il' , 'password': 'A1234567a'}
#         resp = requests.post("http://localhost:3000/signin.php", d)
#         print(resp.text)
#         print(resp)
#         # , allow_redirects=False
#         # Send a request to the mock API server and store the response.
#         # response = requests.get(url)
#         # print(response)
#         # Confirm that the request-response cycle completed successfully.
#         # self.assertTrue(response.ok)
#         self.assertTrue(resp.ok)
#
#
#     # def test_request_about(self):
#     #     url = 'http://localhost:3000/about'
#     #     response = requests.get(url, allow_redirects=False)
#     #     self.assertTrue(response.ok)
#     #
#     # def test_request_instructions(self):
#     #     user_id = '5cd80cf6b8ebba9b30399de4#'
#     #     url = 'http://localhost:3000/user/'+user_id+'instructions'
#     #     response = requests.get(url, allow_redirects=False)
#     #     self.assertTrue(response.ok)
#
#
#
# if __name__ == '__main__':
#     unittest.main()