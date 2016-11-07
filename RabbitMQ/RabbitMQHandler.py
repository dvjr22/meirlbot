############################################################
# file:    RabbitMQHandler.py                              #
# author:  Tyler Moon                                      #
# created: 11/07/2016                                      #
# purpose: This file provides several classes used to      #
# blackbox some of the RabbitMQ messaging procedures to cut#
# down on repeated code                                    #
############################################################
import pika
import uuid
import json

# Base class for all message generating and exchange handling. Call be called
# from other files but is used primarily in the classes below
# TODO: Find a way of hardcoding the exchange names in here and referencing them
# from other files. Similar to a C# or Java enum

class RabbitMQHandler(object):
    def __init__(self, exchange, queueType):
        self.exchange = exchange
        self.queueType = queueType
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, type=queueType)
        print("  [q] Declared an exchanged %r of type %r" % (self.exchange,self.queueType))
    def publishMsg(self, msg, routing_key):
        #msg = ''.join(msg)
        self.channel.basic_publish(self.exchange, routing_key, msg)
        print("  [q] (rabbitMQHandler) Send: %r" % msg)
    def closeConnection(self):
        self.connection.close()

# Class for handling messages to the LogWriter. Simply call
# RabbitMQLogger.logMessage() and pass the log text in as a parameter and that
# text will be written to the log file
class RabbitMQLogger(object):
    def __init__(self):
        self.logHandler = RabbitMQHandler(exchange='logs', queueType='direct')
    def logMessage(self,msg):
        self.logHandler.publishMsg(msg, routing_key='log')
    def closeConnection(self):
        self.logHandler.closeConnection()

# Class for ahdnling database messages to the MongoDBDatabase. The
# databaseMessage function will send a message to the specified collectionName
class RabbitMQDatabase(object):
    def __init__(self,collectionName):
        self.collectionName = collectionName
        self.logHandler = RabbitMQLogger()
        self.databaseHandler = RabbitMQHandler(exchange='database', queueType='topic')
        # TODO: Log this message instead of printing it to std/out
        print("  {/} routing_key = %s" % self.collectionName)
    def databaseMessage(self,msg,operation):
        # TODO: Log this message instead of printing it to std/out
        print('  {/} sending msg %r' % msg)
        routingKey = self.collectionName + "." + operation
        # TODO: Log this message instead of printing it to std/out
        print('collectionName: %s and operation: %s makes routing_key: %s' % (self.collectionName, operation, routingKey))
        self.logHandler.logMessage(msg)
        # Send the message to the database with the right routing key
        self.databaseHandler.publishMsg(msg,routingKey)
    def fetchData(self,msg):
        fetch = RabbitMQFetch()
        returned = fetch.call(msg)
        print('Fetched: %s' % returned)
        return returned
    def closeConnection(self):
        self.logHandler.closeConnection()

# Class for handling RPC (Remote Procedure Call) to the database and then waiting
# for data to be returned
class RabbitMQFetch(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)
    def on_response(self,ch,method,props,body):
        if self.corr_id == props.correlation_id:
            self.response = body
    def call(self,msg):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                    routing_key='database_fetch_queue',
                                    properties=pika.BasicProperties(
                                        reply_to = self.callback_queue,
                                        correlation_id = self.corr_id,
                                    ),
                                    body=msg)
        # TODO: Change this from and inf loop to having some sort of timeout
        while self.response is None:
            self.connection.process_data_events()
        return self.response
