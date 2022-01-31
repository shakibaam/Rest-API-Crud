from flask_restful import Resource
from flask import Flask,request

from models.user import UserModel

class User (Resource) :

    def post(self):
       data = request.get_json()
       user = UserModel(data['role'] , data['username'] , data['password'])


       try:
            user.save_to_db()
            return user.json()
       except:
            return {"message": "An internal error :/"}, 500


class UserList(Resource):

    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
