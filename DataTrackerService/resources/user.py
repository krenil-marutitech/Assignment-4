from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from es import ESKNN

esknn = ESKNN()
result = esknn.create_index()


class FetchMessages(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, text):
        user_id = get_jwt_identity()
        if user_id:
            results = esknn.fetch_messages(text, 'user_message')
            hits = results['hits']['hits']
            if len(hits) > 0:
                messages = []
                for hit in hits:
                    messages.append(hit['_source']['user_message'])

                return {"messages": messages}, 200
            return {"message": "Item not found."}, 404
        return {"message": "Invalid Token."}, 403


class Users(Resource):
    @classmethod
    def get(cls):
        results = esknn.get_all_users()
        users = []
        for user in results['hits']['hits']:
            users.append(user['_source'])
        return {
            "Total": len(users),
            "Users": users
        }, 200

    @classmethod
    # @jwt_required(fresh=True)
    def post(cls):
        data = request.get_json()
        # user_id = get_jwt_identity()
        # if user_id:
        try:
            esknn.insert_user(data)
            return {"Inserted Data": data}, 201
        except Exception as e:
            return {"message": str(e)}, 500
        # return {"message": "Invalid Token"}, 403


class CountMessagesByCategory(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, category):
        user_id = get_jwt_identity()
        if user_id:
            results = esknn.fetch_messages(category, 'category')
            hits = results['hits']['hits']
            if len(hits) > 0:
                count = 0
                for hit in hits:
                    if hit['_source']['user_message']:
                        count += 1
                return {f"Number of messages with category={category}": count}, 200
            return {"message": "category not found."}, 404
        return {"message": "Invalid Token."}, 403


class CountMessagesByDate(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls):
        data = request.get_json()
        user_id = get_jwt_identity()
        if user_id:
            results = esknn.fetch_messages_by_time(data['date'])
            if results == 0:
                return {"message": "Provide 'yyyy-mm-ddTHH:MM:SS' format of date."}, 422
            hits = results['hits']['hits']
            if len(hits) > 0:
                count = 0
                for hit in hits:
                    if hit['_source']['user_message']:
                        count += 1
                return {f"Number of messages with given Date/Time={data['date']}": count}, 200
            return {"message": "Data not found with given date."}, 404
        return {"message": "Invalid Token."}, 403
