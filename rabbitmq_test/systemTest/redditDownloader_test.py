import pika
import json
import uuid
from rabbitmqHandler import rabbitMQHandler

# Produce
def produceLog(msg):
    logHandler = rabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')
    logHandler.publishMsg(msg)
    logHandler.closeConnection()

def produceDatabase():
    databaseHandler = rabbitMQHandler(exchange='database', routing_key='remove', queueType='direct')
    data = {
        'redditId': '594txf',
        'localFile': 'rabbitmqtest',
        'upvotes': 69,
        'url': 'www.rabbitmqtest.com',
        'updateFlag': True
    }
    message = json.dumps(data)
    databaseHandler.publishMsg(message)
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


#channel.start_consuming()

# Request some data from the database
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
findChannel = connection.channel()
result = findChannel.queue_declare(exclusive=True)
callback_queue = result.method.queue


corr_id = ""
response = None
def on_response(ch, method, props, body):
    global response
    response = body



def call(n):
    corr_id = str(uuid.uuid4())
    findChannel.basic_publish(exchange='',
                               routing_key='database_fetch_queue',
                               properties=pika.BasicProperties(
                                     reply_to = callback_queue,
                                     correlation_id = corr_id,
                                     ),
                               body=json.dumps(n))
    while response is None:
        connection.process_data_events()
    return response
findChannel.basic_consume(on_response, no_ack=True, queue=callback_queue)
query = {
    "redditId": "595tr8"
}
print('  [x] Requesting %r' % query)
response = call(query)
print('  [.] Got %r' % response)


produceDatabase()
