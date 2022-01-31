from flask import Flask
from flask_restful import Api
from flask_jwt_extended import *
from flask_jwt import JWT
from recourses.movie import Movie, MovieList
from recourses.comment import Comment, CommentList
from recourses.vote import Vote
from recourses.user import User , UserList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'shakiba'
api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()



api.add_resource(Movie ,'/movie/<int:id>' , '/admin/movie' , '/admin/movie/<int:id>' )
api.add_resource(MovieList , '/movies')
api.add_resource(Vote , '/user/vote')
api.add_resource(Comment ,'/user/comment' , '/admin/comment/<int:id>')
api.add_resource(CommentList , '/comments')
api.add_resource(User , '/register')
api.add_resource(UserList , '/users')



if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
