import pika

# Connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# Get the channel object from the connection
channel = connection.channel()

# Make sure a queue called 'hello' exists. If not then this will create one
channel.queue_declare(queue='hello')

# Send a hello world message
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

print(" [x] Sent 'Hello World!'")

# Close the connection
connection.close()
