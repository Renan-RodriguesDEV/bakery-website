from contextlib import contextmanager

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.configs.config_db import configs_db
from src.utils.uteis import Logger

Logger.info(f"Connecting with {configs_db['connection_url']}")


class DatabaseHandler:
    def __init__(
        self,
        connection_url=configs_db["connection_url"],
    ):
        self.__str_url = connection_url
        self.__engine = create_engine(self.__str_url, echo=True)
        self.session = None

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


@contextmanager
def get_connection():
    try:
        print("Open connection")
        connection = psycopg2.connect(configs_db["connection_url"])
        yield connection
    except Exception as e:
        print(f"Erro in connection: {str(e)}")
    finally:
        print("Closing connection")
        connection.close()
