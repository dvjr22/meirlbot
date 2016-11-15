import pika
import logging
from logging.config import fileConfig
import sys
import os


# Define the connection globally so that the start_consuming can be called
# outside of the main function
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# The function handles the incoming rabbitmq messages and writes them to the log file
def main():
    logging.basicConfig(filename='systemTest.log', level=logging.DEBUG)

    # Connect to the exchange that all the processes are sending their log msgs
    channel.exchange_declare(exchange='logs',type='direct')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name, routing_key='log')

    print('  [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print("  [x] Received: %r" % body)
        # Log the message to the log file
        logging.info("  [x] Received: %r" % body)

    channel.basic_consume(callback, queue=queue_name,no_ack=True)




#line = "  "
#while line:
    #if line == 'stop\n':
    #    print 'Stopping logFileWriter....'
    #    sys.exit(0)
    #else:
main()
channel.start_consuming()
#    line = sys.stdin.readline()

# Start consuming messages after defining the while loop so that a simple 'stop'
# from the stdin can stop the script. This is to avoid KeyboardInterrupt errors
# and so that the MemeExchange can stop the script
