
import pika
import random
import sys
import time

def establish_connection():
    conn_params = pika.ConnectionParameters(host = 'rabbitmq')
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare('randqueue')
    return connection, channel

def post_number_to_queue(channel, max_sleep = 5):
    sleep_time = random.randint(1, max_sleep)
    time.sleep(sleep_time)
    num = random.randint(-sys.maxsize - 1, sys.maxsize)
    channel.basic_publish(exchange = '', routing_key = 'randqueue', body = str(num))
    print('Published number to queue', flush = True)

if __name__ == '__main__':
    while True:
        print('Started cycle', flush = True)
        try:
            print('Hello', flush = True)
            time.sleep(5)
            connection, channel = establish_connection()
            while True:
                post_number_to_queue(channel)
        except pika.exceptions.ConnectionClosed:
            time.sleep(5)
            print('Sorry, connection was closed', flush = True)

    connection.close() 
