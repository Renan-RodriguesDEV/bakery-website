import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    DECIMAL,
    TEXT,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from src.utils.uteis import Logger
from src.utils.hasher import Hasher
from streamlit import secrets


_USERNAME = secrets["USER_DB"]
_PASSWORD = secrets["PASSWORD_DB"]
_HOST = secrets["HOST_DB"]
_DATABASE = secrets["DATABASE_NAME"]


class DatabaseHandler:

    def __init__(
        self, user=_USERNAME, password=_PASSWORD, host=_HOST, database=_DATABASE
    ):
        __user = user
        __password = password
        __host = host
        __database = database
        self.__str_url = f"mysql+pymysql://{__user}:{__password}@{__host}/{__database}"
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


Base = declarative_base()


class Produto(Base):
    __tablename__ = "produtos"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", TEXT(500), nullable=False)
    preco = Column("preco", DECIMAL(15, 2), nullable=False)
    estoque = Column("estoque", Integer, nullable=False)

    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255))
    cpf = Column("cpf", String(255), nullable=True, unique=True)
    telefone = Column("telefone", String(15), nullable=True)
    email = Column("email", String(255), nullable=True)
    token = Column("token", String(255), nullable=True)

    def __init__(self, nome, cpf=None, telefone=None, email=None, token=None):
        self.nome = nome
        self.cpf = Hasher().hasherpswd(cpf) if cpf else None
        self.telefone = telefone
        self.email = email
        self.token = token


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    senha = Column("senha", TEXT(500), nullable=True)  # Increased length for hash

    def __init__(self, nome, email, senha=None):
        self.nome = nome
        self.email = email
        self.senha = Hasher().hasherpswd(senha) if senha else None


class Cliente_Produto(Base):
    __tablename__ = "cliente_produto"
    id = Column(
        "id", Integer, primary_key=True, autoincrement=True
    )  # Adiciona chave primária
    id_cliente = Column("id_cliente", ForeignKey("clientes.id"), nullable=False)
    id_produto = Column("id_produto", ForeignKey("produtos.id"), nullable=False)
    preco = Column("preco", DECIMAL(15, 2))
    quantidade = Column(
        "quantidade",
        Integer,
    )
    total = Column("total", DECIMAL(15, 2))
    data = Column("data", TIMESTAMP, server_default=func.now())

    def __init__(
        self,
        id_cliente,
        id_produto,
        preco,
        quantidade,
        total=0,
        data=datetime.datetime.now(),
    ):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.preco = preco
        self.quantidade = quantidade
        self.total = total
        self.data = data


class Divida(Base):
    __tablename__ = "dividas"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("id_cliente", ForeignKey("clientes.id"), nullable=False)
    valor = Column("valor", DECIMAL(15, 2), nullable=False, default=0)
    pago = Column("pago", DECIMAL(15, 2), nullable=False, default=0)
    data_modificacao = Column("data_modificacao", TIMESTAMP, server_default=func.now())

    def __init__(self, cliente, valor):
        self.id_cliente = cliente.id
        self.valor = valor
        self.data_modificacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def initialize_database():
    with DatabaseHandler() as database_handler:
        # Criação das tabelas no banco de dados
        Base.metadata.create_all(database_handler.get_engine())
        Logger.info("[INFO] - Initialization database sucessfully - [INFO]")
        result = database_handler.session.query(User).filter_by(nome="root").first()
        if not result:
            user = User("root", secrets["USER"], "superuser")
            database_handler.session.add(user)
            database_handler.session.commit()
            Logger.sucess(f"[INFO] User {user.nome} added successfully [INFO]")
