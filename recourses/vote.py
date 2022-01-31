from flask_restful import Resource, reqparse
from flask import Flask,request
from flask_jwt import jwt_required
from models.vote import VoteModel
from functools import wraps
from functools import wraps
from models.user import UserModel
import jwt

class Vote(Resource) :


    def user_exist(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return {
                           "message": "JWT is missing!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401

            else:
                return f(*args, **kwargs)

        return decorated


    @user_exist
    def post(self):
       data = request.get_json()
       token = request.headers["Authorization"].split(" ")[1]
       token = jwt.decode(token, verify=False)
       print(token['user_id'])
       vote = VoteModel(data['movie_id'] , data['vote'] , token['user_id'])



       try:
            vote.save_to_db()
            return vote.json() , 201
       except:
            return {"message": "An internal error occurred :(( ."}, 500






