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

# esknn = ESKNN()
# result = esknn.create_index()
#
#
# @app.route('/api/add_user', methods=["POST"])
# def add_user():
#     data = flask.request.json
#
#     esknn.insert_user(data)
#
#     return jsonify(
#         {
#             "status": 200
#         }
#     )
#
#
# @app.route('/api/search_user')
# def search_user():
#     data = flask.request.json
#
#     field_name = data['field_name']
#     query = data['query']
#
#     results = esknn.search_user(query, field_name)
#
#     documents = []
#
#     hits = results['hits']['hits']
#
#     for hit in hits:
#         documents.append(hit['_source'])
#
#     return {
#         "status": 200,
#         "documents": documents
#     }
api.add_resource(Users, '/api/user')
api.add_resource(FetchMessages, '/api/search/<string:text>')
api.add_resource(CountMessagesByCategory, '/api/msg_count_by_category/<string:category>')
api.add_resource(CountMessagesByDate, '/api/msg_count_by_date')


if __name__ == "__main__":
    app.run(host='localhost', port=9090, debug=True)
