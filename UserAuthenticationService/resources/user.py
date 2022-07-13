import uuid
import re
import json

from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token

from redis_config import redis_client


class Register(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()

        random_id = str(uuid.uuid4().hex)  # generated random unique id
        data['id'] = random_id
        username = data['username']
        password = data['password']

        # regex validation for username and password
        is_valid_username = re.match("^([a-zA-Z0-9_-]{5,15})$", username)
        is_valid_password = re.match("^([a-zA-Z0-9@*#]{6,12})$", password)

        if is_valid_username:
            if is_valid_password:
                red = json.dumps(data)  # python<dict> to string
                newId = username + "_user"  # custom key
                if not redis_client.hget('temps', newId):
                    redis_client.hset('temps', newId, red)
                    return {"message": "Successfully registered."}, 201
                return {"message": "Username already exists"}, 400
            return {"message": "Enter a valid password"}, 400
        return {"message": "Enter a valid username"}, 400


class Login(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()

        username = data['username']
        password = data['password']
        key = username + "_user"

        user = redis_client.hget('temps', key)  # get data from redis
        if user:
            user = json.loads(user)  # convert it back to dictionary type

            # checking user credentials
            if user['username'] == username and user['password'] == password:
                # create access token
                access_token = create_access_token(identity=user['id'], fresh=True)
                # create refresh token
                refresh_token = create_refresh_token(identity=user['id'])
                return {
                    "message": "Successfully logged in.",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200
            return {"message": "Invalid credentials"}, 401
        return {"message": "Please register first."}, 400
