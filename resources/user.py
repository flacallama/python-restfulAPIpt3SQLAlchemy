import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type=str,
        required=True,
        help="this field cannot be left blank"
    )
    parser.add_argument('password',
        type=str,
        required=True, #all requests must have prices
        help="this field cannot be left blank"
    )



    def post(self):
        data = UserRegister.parser.parse_args()

        # CHECK IF USER ALREADY EXISTS - must be before the rest of route
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        

        # # EVERYTHING BELOW IS PRE SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password'],))
        #
        # connection.commit()
        # connection.close()

        return {"message": "User created successfully."}, 201
