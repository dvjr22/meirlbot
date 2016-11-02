import pika

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
        self.channel.basic_publish(self.exchange, self.routing_key, msg)
        print("  [q] (rabbitMQHandler) Send: %r" % msg)
    def closeConnection(self):
        self.connection.close()
