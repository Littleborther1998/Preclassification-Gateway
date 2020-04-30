from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be empty')
    parser.add_argument('store_id', type=int, required=True, help='Every item requires a store')    

    @jwt_required()
    def get(self, name): 
        item =  ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': "An Item with name '{}' was not found".format(name)}, 404        
    
    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An Item with name '{}' already exists".format(name)}, 400 

        data = Item.parser.parse_args()
       
        item =  ItemModel(name, **data)

        try:
            item.save_to_db()
            return item.json(), 201
        except:
            return {'message': "An error has occured inserting '{}'".format(name)},500
 
    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json(), 201

    @jwt_required()        
    def delete(self, name):
        item =  ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': "Item '{}' was deleted".format(name)}, 200
        
class Items(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
       
        

 