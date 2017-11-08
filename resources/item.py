import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True, #all requests must have prices
        help="this field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            # return item
            return item.json() #since models.item.py, we must convert it to a dictionary
        return {'message': 'Item not found'}, 404

        # ALL OF THIS WAS BEFORE DB
        # # lets update this...
        # # for item in items:
        # #     if item['name'] == name:
        # #         return item
        #
        # # USING FILTER()
        # # item = filter(lambda x: x['name'] == name, items)
        # # filter takes 2 arguments - the lambda function, and the list of whats being filtered
        # # the filter function might return more than one item, or no items, in a 'filter object'
        # # item = list(filter(lambda x: x['name'] == name, items))
        # # this would give us the complete list of all items in the list
        # item = next(filter(lambda x: x['name'] == name, items), None) #give us only first item
        # # next throws an error if there are no objects, so we put in None.
        # return {"item": item}, 200 if item else 404 #updated this to turnary

    # @classmethod # moved to models directory
    # def find_by_name(cls, name):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM items WHERE name=?"
    #     result = cursor.execute(query, (name,))
    #     row = result.fetchone()
    #     connection.close()
    #
    #     if row:
    #         return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if ItemModel.find_by_name(name): # or call Item.find_by_name(name)
            return {'message': "an item with name {} already exists.".format(name)}, 400
            # 400 - something went wrong with the request

        data = Item.parser.parse_args()
        # WE DID HAVE THE FOLLOWING LINES HERE BUT WE NEED THE SAME IN PUT ROUTE
        # item = {'name': name, 'price': data['price']}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?,?)"
        # cursor.execute(query, (item['name'], item['price']))
        #
        # connection.commit()
        # connection.close()

        # ^^ let's use this instead to tie in the class method

        # since models.item.py - we need to convert this to an ItemModel object
        # item = {'name': name, 'price': data['price']}
        git  = ItemModel(name, data['price'])

        # if there's an exception use this:
        try:
            # since models.item.py, we now have an ItemModel (see 5 lines above). We can insert into DB
            # ItemModel.insert(item)
            item.save_to_db()  #this is slightly easier
        except:
            return {"message": "An error occurred inserting the item"}, 500 #internal server error
            # 500 - something went wrong, we don't know what, it's not clients fault

        # self.insert(item) - now we don't need this

        return item.json(), 201

    # @classmethod  #moved to models directory
    # def insert(cls, item):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "INSERT INTO items VALUES (?,?)"
    #     cursor.execute(query, (item['name'], item['price']))
    #
    #     connection.commit()
    #     connection.close()





        # # LETS UPDATE THIS TO USE THE CLASS METHOD find_by_name AND GET READY FOR ITEM.PY TRANSFER
        # # ^^ EVERYTHING BELOW IS PART OF THIS
        # # LETS UPDATE THIS POST TO HANDLE A PREVIOUSLY INSERTED ITEM
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "an item with name {} already exists.".format(name)}, 400 #badrequest
        # # lets change the data to user the parser...
        # data = Item.parser.parse_args() # old data request below
        # # data = request.get_json() #this will give an error without params if header is wrong
        # # data = request.get_json(force=True)  #here we don't look at header
        # # data = request.get_json(silent=True) #doesnt give error
        # item = {'name': name, 'price': data['price']}
        # items.append(item)
        # return item, 201 # 201 is for "created"   202 is accepted/delaying created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        # # EVERTHING BELOW IS PRE SQLALCHMY
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()


        # # BELOW IS THE PRE DB VERSION - in memory storage
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # since models.ItemModel.py - lets refactor
        # updated_item = {'name': name, 'price': data['price']}
        # ALCHEMYPHASE updated_item = ItemModel(name, data['price'])


        if item is None:
            item = ItemModel(name, data['price'])
            # # ALCHEMYPHASE - NEXT 5 LINES
            # try:
            #     # ItemModel.insert(updated_item)
            #     updated_item.insert()
            # except:
            #     return {"message": "an error occured inserting the item"}, 500
        else:
            item.price = data['price']
            # # ALCHEMYPHASE - NEXT 5 LINES
            # try:
            #     # ItemModel.update(updated_item)
            #     updated_item.update()
            # except:
            #     return {"message": "an error occured updating the item"}, 500

        item.save_to_db() # part of SQLALCHMY

        # return updated_item

        return item.json()

    # @classmethod    #moved to models directory
    # def update(cls, item):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items SET price=? WHERE NAME=?"
    #     cursor.execute(query, (item['price'], item['name']))
    #
    #     connection.commit()
    #     connection.close()
    #


        # # ALL BELOW IS PRE DB from put route
        # # # this route needs to be parsed bc we can update a Name and Price simulatenously
        # # # lets use reqparse to control what gets updated
        # # # ... actually, let's cut it from here and let the whole class use parser
        # # # we do that by adding "item." in front of parser.parse_args()
        # # parser = reqparse.RequestParser()
        # # parser.add_argument('price',
        # #     type=float,
        # #     required=True, #all requests must have prices
        # #     help="this field cannot be left black"
        # # )
        # # # data = request.get_json()  #lets change this to user parser
        # data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)   # dictionaries have an update method
        # return item

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {"items": items}
