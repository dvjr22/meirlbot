import pika
import time

# Connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# Get the channel object from the connection
channel = connection.channel()

# Make sure a queue called 'hello' exists. If not then this will create one
channel.queue_declare(queue='hello', durable=True)

# Subscribe a callback function from the Pika library to wait for messages
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_ta = method.delivery_tag)

# Tell RabbitMQ that this callback method should recieve messages from our hello queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
