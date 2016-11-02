import pika

# Consume
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bot',type='direct')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bot', queue=queue_name, routing_key='googleDownloader')
print('  [*] Waiting for instructions. To exit press CTRL+C')
def callback(ch, method, properties, body):
    print("  [x] Received: %r" % body)
channel.basic_consume(callback, queue=queue_name,no_ack=True)
channel.start_consuming()
