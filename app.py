from flask import Flask #, request
from flask_restful import Api #, reqparse ,Resource - moved out with classitems
from flask_jwt import JWT #, jwt_required - moved out with classitems

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turns off flask_sqlalchemy modification
#tracker, but not the SQLAlchemy modification tracker. Weird I know.
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

# # the api works with resources, and each resource must be a class
# # ex class Student inherits from Resource
# class Student(Resource):
#     #this is the old way -
#     @app.route('/student...')
#     def get(self, name):
#         return {'student': name}
#
# api.add_resource(Student, '/student/<string:name>')

# items = [] # obsolete

# UP UNTIL SECTION 5, OUR ITEM AND ITEMLIST CLASS RESOURCES WERE HERE

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# if we were to import app.py from another file, it
#would run this app by default. The following line prevents that
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # debug creates a html page for troubleshooting
