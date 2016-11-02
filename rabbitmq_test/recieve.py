import pika

# Connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# Get the channel object from the connection
channel = connection.channel()

# Make sure a queue called 'hello' exists. If not then this will create one
channel.queue_declare(queue='hello')

# Subscribe a callback function from the Pika library to wait for messages
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# Tell RabbitMQ that this callback method should recieve messages from our hello queue
channel.basic_consume(callback, queue='hello', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
