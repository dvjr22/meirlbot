from RabbitMQ.RabbitMQHandler import RabbitMQLogger
# content of test_sample.py

def func(x):
    return x + 1

def test_logger():
    logger = RabbitMQLogger()
    logger.logMessage('test')
    logger.closeConnection()
    with open('./LogWriter/systemTest.log') as f:
      last = None
      for line in (line for line in f if line.rstrip('\n')):
        last = line

    print last

    assert last == 'INFO:root:  [x] Received: \'test\'\n'
