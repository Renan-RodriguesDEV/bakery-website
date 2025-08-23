import json

import pika
from notifications import Notifications


class Publisher(Notifications):
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        super().__init__(host, port, username, password)

    def publish(self, body, exchange="my_exchange", routing_key=""):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2),
        )


try:
    publisher = Publisher()
except pika.exceptions.AMQPConnectionError:
    publisher = None
    print("Failed to connect to RabbitMQ server.")
if __name__ == "__main__":
    if publisher:
        message = json.dumps({"status": "Orders its ok"})
        publisher.publish(message)
