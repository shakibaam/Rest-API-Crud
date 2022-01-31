from db import db
import datetime


class CommentModel(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(80))
    approved = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime)
    MovieID = db.Column(db.Integer , db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, comment,  MovieID , user_id):
        self.comment = comment
        self.approved = False
        self.createdAt = datetime.datetime.now()
        self.MovieID = MovieID
        self.user_id = user_id

    def json(self):
        return {

            'comment': self.comment,
            'movie_id' :self.MovieID,
            'approved': self.approved,
            'user_id' : self.user_id,
            # 'createdAt': self.createdAt,

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
