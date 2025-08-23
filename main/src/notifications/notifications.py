import pika


class Notifications:
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.credentials = pika.PlainCredentials(self.username, self.password)
        self.connection_params = pika.ConnectionParameters(
            self.host, self.port, credentials=self.credentials
        )
        self.channel = self.__create_channel()

    def __create_channel(self):
        blocking_connection = pika.BlockingConnection(self.connection_params)
        return blocking_connection.channel()
