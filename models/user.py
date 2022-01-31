from db import db

class UserModel(db.Model) :
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, role, username , password):

        self.role = role
        self.username = username
        self.password = password

    def json(self):
         return { 'role' :self.role , 'username' :self.username }

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
