from flask_restful import Resource
from flask import Flask, request
from models.comment import CommentModel
from functools import wraps
import jwt


class Comment(Resource):

    def user_exist(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return {
                           "message": "JWT Token is missing!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401

            else:
                return f(*args, **kwargs)

        return decorated

    def just_admin(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return {
                           "message": "Authentication Token is missing!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401

            else:
                token = request.headers["Authorization"].split(" ")[1]
                token = jwt.decode(token, verify=False)

                if (token['admin'] == 1):
                    return f(*args, **kwargs)
                else:
                    return {
                               "message": "You are not Admin :(!",

                           }, 401

        return decorated

    @user_exist
    def post(self):

        data = request.get_json()
        token = request.headers["Authorization"].split(" ")[1]
        token = jwt.decode(token, verify=False)
        print(token['user_id'])

        comment = CommentModel(data['comment_body'], data['movie_id'], token['user_id'])

        comment.save_to_db()

        return comment.json(), 201

    @just_admin
    def delete(self, id):
        comment = CommentModel.find_by_id(id)
        if comment:
            try:
                comment.delete_from_db()
                return {'message': 'comment deleted.'}, 201
            except:
                return {"message": "An internal error :/ ."}, 500
        return {'message': 'comment not found :((.'}, 404

    @just_admin
    def put(self, id):
        comment = CommentModel.find_by_id(id)
        data = request.get_json()
        if comment:
            try:
                comment.approved = data['approved']
                comment.save_to_db()
                return {"message": "Comment updated"}, 201

            except:
                return {"message": "An internal error :/ "}, 500
        return {'message': 'comment not found :(( '}, 404


class CommentList(Resource):

    def get(self):
        return {'comments': list(map(lambda x: x.json(), CommentModel.query.all()))}
