# import pika
#
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='myqueue')
#
#
# def callback(ch, method, property, body):
#     print("[x] received %r" %body)
#
#
# channel.basic_consume(queue="myqueue", on_message_callback=callback, auto_ack=True)
#
# channel.start_consuming()
