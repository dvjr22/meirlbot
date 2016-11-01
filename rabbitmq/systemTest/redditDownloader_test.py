import pika
from rabbitmqHandler import rabbitMQHandler

# Produce
def produceLog(msg):
    logHandler = rabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')
    logHandler.publishMsg(msg)
    logHandler.closeConnection()

def produceDatabase():
    databaseHandler = rabbitMQHandler(exchange='database', routing_key='update', queueType='direct')
    databaseHandler.publishMsg('  [x] (redditDownloader) Send: This is an update msg from redditDownloader')
    databaseHandler.closeConnection()

def callGoogleDownloader(msg):
    googleHandler = rabbitMQHandler(exchange='bot', routing_key='googleDownloader', queueType='direct')
    googleHandler.publishMsg('  [x] (redditDownloader) Send: This is a message from redditDownloader :: Original Message: %r' % msg)
    googleHandler.closeConnection()

# Consume
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='bot',type='direct')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='bot', queue=queue_name, routing_key='redditDownloader')
print('  [*] Waiting for instructions. To exit press CTRL+C')
def callback(ch, method, properties, body):
    print("  [x] (redditDownloader) Received: %r" % body)
    print("  [x] (redditDownloader) Send: On to googleDownloader")
    produceLog("  [x] (redditDownloader) Received: %r" % body)
    produceDatabase()
    callGoogleDownloader(body)
channel.basic_consume(callback, queue=queue_name,no_ack=True)
channel.start_consuming()
