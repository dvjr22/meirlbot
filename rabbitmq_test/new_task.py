import pika
import sys

# Connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# Get the channel object from the connection
channel = connection.channel()

# Make sure a queue called 'hello' exists. If not then this will create one
channel.queue_declare(queue='hello')

# Send a hello world message
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                        delivery_mode = 2, # Make messages persistant
                      ))

print(" [x] Sent %r" % message)

# Close the connection
connection.close()
