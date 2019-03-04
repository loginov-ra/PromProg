
import pika
import time
import sys

def callback(ch, method, properties, body):
    print('Received:', body, flush = True)

def establish_connection():
    conn_params = pika.ConnectionParameters(host = 'rabbitmq')
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue = 'randqueue')
    return (connection, channel)

if __name__ == '__main__':
    time.sleep(20)
    connection, channel = establish_connection()

    channel.basic_consume(callback, queue = 'randqueue')
    while True:
        try:
            print('Start of consuming', flush = True)
            channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            print('Sorry, connection was closed', flush = True)
            channel.stop_consuming()

    connection.close()
