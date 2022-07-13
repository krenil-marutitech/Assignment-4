import time
import pika
import json
import requests
import random


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials, heartbeat=0))
channel = connection.channel()
channel.queue_declare(queue='myqueue', durable=True)


def callback(ch, method, property, body):
    data_all = json.loads(body)

    # change status according to random_number
    # default category is 'Direct'
    for data in data_all:
        if (data['random_number'] % 10) == 0:
            data['category'] = 'Retried'
            data['random_number'] = random.randint(1, 60)

            # process after 4 seconds
            time.sleep(4)
            if (data['random_number'] % 10) == 0:
                data['category'] = 'Failed'

    response = requests.post("http://127.0.0.1:9090/api/user", json=data_all)
    print("Response: ", response.status_code)
    print("[x] received %r" %data_all)


channel.basic_consume(queue="myqueue", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
