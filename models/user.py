import sqlite3
from db import db  # part of our SQLAlchemy


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, _id, username, password):  # id is a python keyword, so we use _id
        self.id = _id
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):  #cls was 'self' before we went to classmethod'
        return cls.query.filter_by(username=username).first()

        # # EVERYTHING BELOW IS PRE SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))  #the weird parenthesesis/comma make arg a tupple
        # row = result.fetchone() #returns first row if there is one
        # if row:  #if there is one row
        #     # user = User(row[0], row[1], row[2]) - we'd use this if not an @classmethod
        #     # user = cls(row[0], row[1], row[2])  - this is a good option, but lets clean it up
        #     user = cls(*row)  #the most clean
        # else:
        #     user = None
        #
        # connection.close()
        # return user


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # # EVERYTHING BELOW IS PRE SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user
