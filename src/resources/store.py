from flask_restful import Resource
from src.models.store import  StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store {} does not exist". format(name)}, 404 # Requested data not found

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "A store named '{}' already exists!".format(name)}, 400 # Bad request for data

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "The was an error inserting the store in database"}, 500  # Internal error

        return store.json(), 201   # Successfully created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}

