import pika
import json
from pymongo import MongoClient
import pymongo
from bson import BSON
from bson import json_util
from rabbitmqHandler import rabbitMQHandler

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.redditposts

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# RabbitMQ log queue
logHandler = rabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')


# Database Remove
removeChannel = connection.channel()
removeChannel.exchange_declare(exchange='database',type='direct')
result = removeChannel.queue_declare(exclusive=True)
queue_name = result.method.queue
removeChannel.queue_bind(exchange='database', queue=queue_name, routing_key='remove')
print('  [*] Waiting for database instructions. To exit press CTRL+C')
def removeCallback(ch, method, properties, body):
    print("  [x] Received: %r" % body)
    data = json.loads(body)
    redditID = ""
    try:
        redditID = data['redditId']
        rposts.remove({"redditId": redditID},False)
        logHandler.publishMsg('  [x] (databaseHandler) Removed %r from the database' % body)
    except Exception as e:
        logHandler.publishMsg('  [x] (databaseHandler) Error in databaseHandler remove: %s' % e)
removeChannel.basic_consume(removeCallback, queue=queue_name,no_ack=True)


# Database Update
updateChannel = connection.channel()
updateChannel.exchange_declare(exchange='database',type='direct')
result = updateChannel.queue_declare(exclusive=True)
queue_name = result.method.queue
updateChannel.queue_bind(exchange='database', queue=queue_name, routing_key='update')
print('  [*] Waiting for database instructions. To exit press CTRL+C')
def updateCallback(ch, method, properties, body):
    print("  [x] Received: %r" % body)
    data = json.loads(body)
    redditID = ""
    try:
        # Database updating here
        redditID = data['redditId']
        rposts.update_one({"redditId": redditID}, { '$set': data})
        # Publish to the log queue that the database was updated
        logHandler.publishMsg('  [x] (databaseHandler) Updated the database with %r' % body)
    except Exception as e:
        # Publish any exceptions encountered
        logHandler.publishMsg('  [x] (databaseHandler) Error in databaseHandler update: %s' % e)
        print('Error %s' % e)
updateChannel.basic_consume(updateCallback, queue=queue_name,no_ack=True)


# Database Find
# Using an RPC architecture to return data to the calling process
findChannel = connection.channel()
findChannel.queue_declare(queue='database_fetch_queue')
def findData(query):
    return rposts.find(json.loads(query))

def on_request(ch, method, props, body):
    logHandler.publishMsg('  [x] (databaseHandler) Received: %s' % json.loads(body))
    response = findData(body)
    json_response = "Error"
    try:
        json_response = json.dumps(response[0], default=json_util.default)
    except:
        logHandler.publishMsg('  [x] (databaseHandler) Error parsing json')
    logHandler.publishMsg('  [x] (databaseHandler) Returning response: %r' % json_response)
    ch.basic_publish(exchange='',routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id=props.correlation_id),body=json_response)

    ch.basic_ack(delivery_tag = method.delivery_tag)

findChannel.basic_qos(prefetch_count=1)
findChannel.basic_consume(on_request, queue='database_fetch_queue')


# Start consuming from the queues and wait for new items to come in
updateChannel.start_consuming()
removeChannel.start_consuming()

# Close the connections to avoid potential memory leaks
connection.close()
logHandler.closeConnection()
