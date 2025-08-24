import json

import pika
from utilities import check

from notifications import Notifications


class Publisher(Notifications):
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        super().__init__(host, port, username, password)

    def publish(self, body, exchange="my_exchange", routing_key=""):
        print(f"Publishing message: {body}")
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
        try:
            results = check()
        except Exception as e:
            print(f"Error checking database: {e}")
            results = []
        for result in results:
            # message = json.dumps({"status": "Orders its ok"})
            message = json.dumps(
                {
                    "status": "warning" if result.get("estoque") > 0 else "danger",
                    "message": f"Orders {result.get('nome')} its don't ok",
                }
            )
            publisher.publish(message)
        publisher.channel.close()
