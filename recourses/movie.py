from flask_restful import Resource, reqparse
from models.movie import MovieModel
from flask import Flask,request
from flask_jwt_extended import *
from functools import wraps
from models.user import UserModel
import jwt

class Movie(Resource):


    def just_admin(f):
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
                token = request.headers["Authorization"].split(" ")[1]
                token = jwt.decode(token, verify=False)
                if (token['admin'] == 1):
                    return f(*args, **kwargs)
                else:
                    return {
                               "message": "You are not Admin :(!",

                           }, 401

        return decorated


    def get(self, id):
        movie = MovieModel.find_by_id(id)
        if movie:
            return movie.json()
        return {'message': 'movie not found :(('}, 404




    @just_admin
    def post(self):

        data = request.get_json()
        name = data['name']
        description = data['description']


        movie = MovieModel(name, description)
        try:
            movie.save_to_db()
        except:
            return {"message": "An internal error :/"}, 500

        return movie.json(), 201


    @just_admin
    def delete(self, id):
        movie = MovieModel.find_by_id(id)
        if movie:
            try:
                movie.delete_from_db()
                return {'message': 'Movie deleted.'}, 201
            except:
                return {"message": "An internal error :/"}, 500
        else:
            return {'message': 'movie not found :(('}, 404


    @just_admin
    def put(self, id):
        data = request.get_json()

        movie = MovieModel.find_by_id(id)

        if movie:
            try:
                movie.name = data['name']
                movie.description = data['description']
                movie.save_to_db()
                return movie.json() , 201
            except:
                return {"message": "An internal error :/"}, 500
        else:
            return {'message': 'movie not found :(('}, 404


class MovieList(Resource):

    def get(self):
        return {'movies': list(map(lambda x: x.json(), MovieModel.query.all()))}
