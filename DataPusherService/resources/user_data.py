import json
import random
import pika
import datetime

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from redis_config import redis_client


class Message(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        data = request.get_json()
        user_id = get_jwt_identity()
        if user_id:
            try:
                # request counter
                prev_count = redis_client.hget('tc', user_id)
                if prev_count:
                    incr_by_1 = int(prev_count) + 1
                    redis_client.hset('tc', user_id, incr_by_1)
                else:
                    redis_client.hset('tc', user_id, 1)

                req_count = int(redis_client.hget('tc', user_id))
            except:
                return {"message": "Some error occurred in counting no. of requests."}, 500

            # current date and time
            current_time = datetime.datetime.now()
            current_time = str(current_time.strftime("%Y-%m-%dT%H:%M:%S"))

            # set other properties
            for i_data in data:
                i_data['user_id'] = user_id
                i_data['random_number'] = random.randint(1, 60)
                i_data['request_count'] = req_count
                i_data['created_time'] = current_time
                i_data['category'] = 'Direct'

            # <dict> to <string>
            data = json.dumps(data)

            try:
                # send data to validator using rabbitmq
                credentials = pika.PlainCredentials('admin', 'admin')
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters('localhost', credentials=credentials, heartbeat=0))
                channel = connection.channel()
                channel.queue_declare(queue='myqueue', durable=True)
                channel.basic_publish(exchange="", routing_key="myqueue", body=data)
                connection.close()
            except:
                return {"message": "Some error occurred in sending messages."}, 500

            return {"message": "Messages are sent."}, 201
        return {"message": "Invalid Token."}, 403

        # header = request.headers['Authorization']
        # token1 = header.split(" ")[1]
        # data1 = jwt.decode(token1, JWT_SECRET_KEY, algorithms=['HS256'])
