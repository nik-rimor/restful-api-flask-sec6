from flask import Flask
from flask_restful import  Api
from flask_jwt_extended import JWTManager
from src.security import EntityLogin
from src.resources.user import UserRegister
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "tiskarotsastakarouliaotantrexeikanounr"
app.config['JWT_SECRET_KEY'] = "tiskarotsastakarouliaotantrexeikanounr"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

api.add_resource(EntityLogin, '/login')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from src.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
