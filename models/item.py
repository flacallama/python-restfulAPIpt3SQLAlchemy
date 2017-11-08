# import sqlite3
from db import db  # part of our SQLAlchemy


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):  #this is what returns our json object
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # return ItemModel.query.filter_by(name=name).first()
        # select * from items where name=? limit 1  ^^

        # # EVERTHING BELOW IS FROM PRE SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     # return cls(row[0], row[1])
        #     return cls(*row) #unpacks. same as ^^

    # def insert(self): now we have a new name
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

        # # EVERTHING BELOW IS FROM PRE SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?,?)"
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()

    # def update(self):
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        # # EVERTHING BELOW IS FROM PRE SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "UPDATE items SET price=? WHERE NAME=?"
        # cursor.execute(query, (self.price, self.name))
        #
        # connection.commit()
        # connection.close()
