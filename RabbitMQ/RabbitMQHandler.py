import pika
import uuid
import json

class RabbitMQHandler(object):
    def __init__(self, exchange, routing_key, queueType):
        self.exchange = exchange
        self.routing_key = routing_key
        self.queueType = queueType
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, type=queueType)
        print("  [q] Declared an exchanged %r of type %r" % (self.exchange,self.queueType))
    def publishMsg(self, msg):
        #msg = ''.join(msg)
        self.channel.basic_publish(self.exchange, self.routing_key, msg)
        print("  [q] (rabbitMQHandler) Send: %r" % msg)
    def closeConnection(self):
        self.connection.close()

class RabbitMQLogger(object):
    def __init__(self):
        self.logHandler = RabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')
    def logMessage(self,msg):
        self.logHandler.publishMsg(msg)
    def closeConnection(self):
        self.logHandler.closeConnection()

class RabbitMQDatabase(object):
    def __init__(self,collectionName):
        self.collectionName = collectionName
        self.logHandler = RabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')
        self.databaseHandler = RabbitMQHandler(exchange='database', routing_key=self.collectionName, queueType='direct')
        print("  {/} routing_key = %s" % self.collectionName)
    def databaseMessage(self,msg):
        print('  {/} sending msg %r' % msg)
        self.logHandler.publishMsg(msg)
    def fetchData(self,msg):
        fetch = RabbitMQFetch()
        returned = fetch.call(msg)
        print('Fetched: %s' % returned)
        return returned
    def closeConnection(self):
        self.logHandler.closeConnection()

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
        while self.response is None:
            self.connection.process_data_events()
        return self.response
