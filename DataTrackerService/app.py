# import flask
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import Users, FetchMessages, CountMessagesByCategory, CountMessagesByDate

# from es import ESKNN


app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_SECRET_KEY'] = 'verysecret'
jwt = JWTManager(app)
api = Api(app)

api.add_resource(Users, '/api/user')
api.add_resource(FetchMessages, '/api/search/<string:text>')
api.add_resource(CountMessagesByCategory, '/api/msg_count_by_category/<string:category>')
api.add_resource(CountMessagesByDate, '/api/msg_count_by_date')


if __name__ == "__main__":
    app.run(host='localhost', port=9090, debug=True)
