from db import db


class MovieModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    votes = db.relationship('VoteModel', lazy='dynamic')
    comments = db.relationship('CommentModel', lazy='dynamic')

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def average_rating(self):
        avg = 0
        counter = 0
        flag = False

        for rate in self.votes :
            flag = True
            avg += rate.rating
            counter += 1
        if(flag):
            return avg/counter
        else:
            return 0


    def json(self):
        return { 'name' :self.name ,'description' :self.description ,'rating' :self.average_rating() , 'comments' : [comment.json() for comment in self.comments.all()]}

    @classmethod

    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()