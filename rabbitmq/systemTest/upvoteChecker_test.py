import pika
from rabbitmqHandler import rabbitMQHandler

for _ in range(0,1000):
    logHandler = rabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')
    logHandler.publishMsg('  [x]  This is a log from upvoteChecker')

    databaseHandler = rabbitMQHandler(exchange='database', routing_key='update', queueType='direct')
    databaseHandler.publishMsg('  [x] This is an update msg from upvoteChecker')

    botHandler = rabbitMQHandler(exchange='bot', routing_key='redditDownloader', queueType='direct')
    botHandler.publishMsg('  [x] This is a message from upvoteChecker')

    logHandler.closeConnection()
    databaseHandler.closeConnection()
