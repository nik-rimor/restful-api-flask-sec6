from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from src.models.user import UserModel


class EntityLogin(Resource):
    def post(self):
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']
        user = UserModel.find_by_username(username)
        # check the SHA256 hash of given and stored to password to see if they match
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        return {"message": "Invalid Login data"}, 400
