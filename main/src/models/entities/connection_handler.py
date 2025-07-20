from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.configs.config_db import configs_db
from src.utils.uteis import Logger

Logger.info(
    f"{configs_db['username']} {configs_db['password']} {configs_db['host']} {configs_db['database']}"
)


class DatabaseHandler:
    def __init__(
        self,
        user=configs_db["username"],
        password=configs_db["password"],
        host=configs_db["host"],
        database=configs_db["database"],
    ):
        __user = user
        __password = password
        __host = host
        __database = database
        self.__str_url = f"mysql+pymysql://{__user}:{__password}@{__host}/{__database}"
        self.__engine = create_engine(
            self.__str_url,
            #   echo=True
        )
        self.session = None

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
