# import pika
#
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='myqueue')
#
# channel.basic_publish(exchange="", routing_key="myqueue", body="hello")
#
# connection.close()
