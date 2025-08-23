import pika
import pika.exceptions
from notifications import Notifications


class Consumer(Notifications):
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        super().__init__(host, port, username, password)

    def start(self, callback, queue="my_queue"):
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=callback
        )
        self.channel.start_consuming()


def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")


try:
    consumer = Consumer()
except pika.exceptions.AMQPConnectionError:
    consumer = None
    print("Consumer stopped because of connection error.")
if __name__ == "__main__":
    if consumer:
        print("Starting consumer...")
        consumer.start(callback)
