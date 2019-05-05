from flask import request
from flask_restful import Resource

from jobmatcher.server.modules.user.User import User


def checkUserFile(user_id):
    # print("checkUserFile")
    # print("user_id: ")
    # print(user_id)
    user = User.objects.get(pk=user_id)
    if user.cvs == None:
        return True
    return False

