import json
import sys

import pika
import pika.exceptions
from utilities import notify, save_notification

from notifications import Notifications


class Consumer(Notifications):
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        super().__init__(host, port, username, password)

    def start(self, callback, queue="my_queue"):
        print("Starting consumer...")
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=callback
        )
        self.channel.start_consuming()


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    print(f"Received message: {body}")
    print(f"Message type: {type(body)}")
    try:
        dict_body = json.loads(body)
    except Exception as e:
        print(f"Error parsing message {body}: {e}")
        return
    print(f"Message type: {type(body)}")

    status = dict_body.get("status", "").title()
    product = dict_body.get("product", "")
    stock = dict_body.get("stock")
    if not status or not product or stock is None:
        print(f"Invalid message format: {body}")
        return
    message = f"{status} - {product}\nEstoque total: {stock}"
    save_notification(message)
    if "Warning" in status:
        notify(
            f"Atenção, estoque de ({product}) está abaixo do mínimo! em estoque {stock}",
            "warning",
        )
    elif "Danger" in status:
        notify(
            f"Atenção, estoque de ({product}) está esgotado! em estoque ({stock})",
            "danger",
        )


try:
    consumer = Consumer()
except pika.exceptions.AMQPConnectionError:
    consumer = None
    print("Consumer stopped because of connection error.")
if __name__ == "__main__":
    try:
        if consumer:
            print("Starting consumer...")
            consumer.start(callback)
    except KeyboardInterrupt:
        print("Consumer stopped by user.")
        sys.exit(0)
