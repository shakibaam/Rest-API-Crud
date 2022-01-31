
from db import db


class VoteModel(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    MovieID = db.Column(db.Integer , db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, MovieID , rating , user_id):


        self.rating = rating
        self.MovieID = MovieID
        self.user_id = user_id

    def json(self):
        return {

            'movie_id': self.MovieID,
            'user_id' :self.user_id ,
            'rating' : self.rating


        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()