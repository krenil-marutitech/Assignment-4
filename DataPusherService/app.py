from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user_data import Message


app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_SECRET_KEY'] = 'verysecret'
jwt = JWTManager(app)
api = Api(app)

api.add_resource(Message, '/api/send_message')


if __name__ == "__main__":
    app.run(host='localhost', port=9092, debug=True)
