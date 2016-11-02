import pika
import logging
from logging.config import fileConfig

logging.basicConfig(filename='systemTest.log', level=logging.DEBUG)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name, routing_key='log')

print('  [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print("  [x] Received: %r" % body)
    logging.info("  [x] Received: %r" % body)

channel.basic_consume(callback, queue=queue_name,no_ack=True)

channel.start_consuming()
