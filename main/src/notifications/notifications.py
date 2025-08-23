import os

import pika
from dotenv import load_dotenv

load_dotenv()


class Notifications:
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.credentials = pika.PlainCredentials(self.username, self.password)
        self.connection_params = (
            pika.ConnectionParameters(
                self.host, self.port, credentials=self.credentials
            )
            if not os.getenv("RABBITMQ_URL")
            else pika.URLParameters(os.getenv("RABBITMQ_URL"))
        )
        print(self.connection_params)
        self.channel = self.__create_channel()

    def __create_channel(self):
        blocking_connection = pika.BlockingConnection(self.connection_params)
        return blocking_connection.channel()
