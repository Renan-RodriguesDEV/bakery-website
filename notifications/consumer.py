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
    body = body.decode()
    print(f"Received message: {body}")
    print(f"Message type: {type(body)}")
    dict_body = json.loads(body)
    print(f"Message type: {type(body)}")

  
    message = f"{dict_body.get('status')} - {dict_body.get('message')}\nEstoque total: {dict_body.get('stock')}"
    save_notification(message)
    if "warning" in dict_body.get("status", "").lower():
        notify(
            f"Atenção, estoque está abaixo do mínimo! em estoque {dict_body.get('stock')}",
            dict_body.get("message"),
        )
    elif "danger" in dict_body.get("status", "").lower():
        notify(
            f"Atenção, estoque está esgotado! em estoque ({dict_body.get('stock')})",
            dict_body.get("product"),
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
