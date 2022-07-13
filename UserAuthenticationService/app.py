from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import Register, Login


app = Flask(__name__)
api = Api(app)


app.config['JWT_SECRET_KEY'] = 'verysecret'
jwt = JWTManager(app)

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')


if __name__ == "__main__":
    app.run(host='localhost', port=9091, debug=True)
