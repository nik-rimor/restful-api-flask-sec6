from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from src.models.item import ItemModel


class Item(Resource):
    # we move the parser code here so its not duplicated and also belongs to class
    # that is why we call the parser with the Item.parser.parse_args() using the class name
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists.".format(name)}, 400  # Bad Request

        data = Item.parser.parse_args()
        # **data can gives us the unpacked named arguments from the data
        # instead of writing :   item = ItemModel(name, data["price"], data['store_id'])
        # we can write
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201  # we don't have to do jsonify because flask_restful is doing this for us

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted successfully"}, 200

        return {"message": "An item with name {} does not exist.".format(name)}, 400  # Bad Request

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
                item.save_to_db()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
                item.save_to_db()
            except:
                return {"message": "An error occurred updating the item."}, 500

        return item.json(), 201


class ItemList(Resource):
    @jwt_required
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
