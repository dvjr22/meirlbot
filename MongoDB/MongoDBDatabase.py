############################################################
# file:    MongoDBDatabase.py                              #
# author:  Tyler Moon                                      #
# created: 11/07/2016                                      #
# purpose: This script is a consumer of RabbitMQ messages  #
# to handle all the database update, delete, and find      #
# operations                                               #
############################################################
import pika
import json
from pymongo import MongoClient
import pymongo
from bson import BSON
from bson.json_util import dumps
from RabbitMQ.RabbitMQHandler import RabbitMQHandler
from RabbitMQ.RabbitMQHandler import RabbitMQLogger

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.redditposts
uposts = db.upvoteposts

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# RabbitMQ log queue
logHandler = RabbitMQLogger()


# Database Remove
'''
removeChannel = connection.channel()
removeChannel.exchange_declare(exchange='database',type='topic')
result = removeChannel.queue_declare(exclusive=True)
queue_name = result.method.queue
removeChannel.queue_bind(exchange='database', queue=queue_name, routing_key='remove')
print('  [*] Waiting for database instructions. To exit press CTRL+C')
def removeCallback(ch, method, properties, body):
    # TODO: Change this print statement to a logHandler.publishMsg
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
'''

# Database Update
updateChannel = connection.channel()
updateChannel.exchange_declare(exchange='database',type='topic')
result = updateChannel.queue_declare(exclusive=True)
queue_name = result.method.queue
updateChannel.queue_bind(exchange='database', queue=queue_name, routing_key='redditposts.update')
print('  [*] Waiting for database instructions. To exit press CTRL+C')
def updateCallback(ch, method, properties, body):
    # TODO: Change this print statement to a logHandler.publishMsg
    print("  [x] Received: %r" % body)
    data = json.loads(body)
    redditID = ""
    try:
        # Database updating here
        redditID = data['redditId']
        rposts.update_one({"redditId": redditID}, { '$set': data}, True)
        # Publish to the log queue that the database was updated
        logHandler.logMessage('  [x] (databaseHandler) Updated the database with %r' % body)
    except Exception as e:
        # Publish any exceptions encountered
        logHandler.logMessage('  [x] (databaseHandler) Error in databaseHandler update: %s' % e)
        # TODO: Change this print statement to a logHandler.publishMsg
        print('Error %s' % e)
updateChannel.basic_consume(updateCallback, queue=queue_name,no_ack=True)





# Database upvoteposts.update
updateChannel = connection.channel()
updateChannel.exchange_declare(exchange='database',type='topic')
result = updateChannel.queue_declare(exclusive=True)
queue_name = result.method.queue
updateChannel.queue_bind(exchange='database', queue=queue_name, routing_key='upvoteposts.update')
print('  [*] Waiting for database instructions. To exit press CTRL+C')
def updateCallback(ch, method, properties, body):
    # TODO: Change this print statement to a logHandler.publishMsg
    print("  [x] (upvoteposts) Received: %r" % body)
    data = ""
    redditID = ""
    try:
        data = json.loads(body)
        if 'redditId' in data:
            redditID = data['redditId']
    except Exception as e:
        logHandler.logMessage('  [e] (databaseHandler upvoteposts) Error in parsing data %s or type %r' % (e,type(e)))
    try:
        # Database updating here
        uposts.update_one({"redditId": redditID}, { '$set': data},True)
        # Publish to the log queue that the database was updated
        logHandler.logMessage('  [x] (databaseHandler) Updated the database with %r' % body)
    except Exception as e:
        # Publish any exceptions encountered
        logHandler.logMessage('  [x] (databaseHandler) Error in databaseHandler update: %s of the type %r' % (e,type(e)))
updateChannel.basic_consume(updateCallback, queue=queue_name,no_ack=True)





# Database Find
# Using an RPC architecture to return data to the calling process
# Returns data from the mongo query to whoever sent the request
findChannel = connection.channel()
findChannel.queue_declare(queue='database_fetch_queue')
def findData(query):
    # TODO: Change this print statement to a logHandler.publishMsg and add correct log formatting
    print("JSON QUERY: %s" % json.loads(query))
    return dumps(rposts.find(json.loads(query)))
    #return dumps(rposts.find())

def on_request(ch, method, props, body):
    logHandler.logMessage('  [x] (databaseHandler) Received: %s' % str(body))
    response = findData(body)
    json_response = None
    try:
        json_response = response
    except:
        logHandler.logMessage('  [x] (databaseHandler) Error parsing json')
    logHandler.logMessage('  [x] (databaseHandler) Returning response: %r' % json_response)
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
