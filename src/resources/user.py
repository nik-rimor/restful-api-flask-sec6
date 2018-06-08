import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from src.models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )


    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']) is not None:
            return {"message": "User with this name already exists!"}, 400

        password_hash = generate_password_hash(data['password'])
        user = UserModel(data['username'], password_hash)
        user.save_to_db()

        return {"message": "User created successfully"}, 201
