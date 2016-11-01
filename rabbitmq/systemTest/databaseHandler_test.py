import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
# Remove
removeChannel = connection.channel()

removeChannel.exchange_declare(exchange='database',type='direct')

result = removeChannel.queue_declare(exclusive=True)
queue_name = result.method.queue

removeChannel.queue_bind(exchange='database', queue=queue_name, routing_key='remove')

print('  [*] Waiting for database instructions. To exit press CTRL+C')

def removeCallback(ch, method, properties, body):
    print(" [x] Received: %r" % body)

removeChannel.basic_consume(removeCallback, queue=queue_name,no_ack=True)


# Update
updateChannel = connection.channel()

updateChannel.exchange_declare(exchange='database',type='direct')

result = updateChannel.queue_declare(exclusive=True)
queue_name = result.method.queue

updateChannel.queue_bind(exchange='database', queue=queue_name, routing_key='update')

print('  [*] Waiting for database instructions. To exit press CTRL+C')

def updateCallback(ch, method, properties, body):
    print(" [x] Received: %r" % body)

updateChannel.basic_consume(updateCallback, queue=queue_name,no_ack=True)

updateChannel.start_consuming()
removeChannel.start_consuming()
