import datetime
import os
import sys
from typing import Literal
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    DECIMAL,
    TEXT,
    Enum,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from src.models.entities.connection_handler import DatabaseHandler


# sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from src.utils.uteis import Logger
from src.utils.hasher import Hasher
from src.models.configs.config_geral import configs


Base = declarative_base()


class Produto(Base):
    __tablename__ = "produtos"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", TEXT(500), nullable=False)
    preco = Column("preco", DECIMAL(15, 2), nullable=False)
    categoria = Column(
        "categoria", Enum("Bebidas", "Doces", "Salgados", "Padaria", "Mercearia")
    )
    estoque = Column("estoque", Integer, nullable=False)

    def __init__(
        self,
        nome,
        preco,
        categoria: Literal["Bebidas", "Doces", "Salgados", "Padaria", "Mercearia"],
        estoque,
    ):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
        self.estoque = estoque

    def __str__(self):
        return f"Produto(id={self.id}, nome='{self.nome}', preco={self.preco}, categoria='{self.categoria}', estoque={self.estoque})"


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255))
    cpf = Column("cpf", String(255), nullable=True, unique=True)
    senha = Column("senha", String(255), nullable=False)
    telefone = Column("telefone", String(15), nullable=True)
    email = Column("email", String(255), nullable=True, unique=True)
    token = Column("token", String(255), nullable=True)
    activate = Column("activate", Boolean, nullable=False, server_default="1")

    def __init__(self, nome, cpf, telefone, email, senha=None, token=None):
        self.nome = nome
        self.cpf = cpf
        if not senha:
            senha = self.cpf
        self.senha = Hasher().hasherpswd(senha) if senha else None
        self.telefone = telefone
        self.email = email
        self.token = token
        self.activate = 1

    def __str__(self):
        return f"Cliente(id={self.id}, nome='{self.nome}', cpf='{self.cpf}', telefone='{self.telefone}', email='{self.email}')"


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255), nullable=False)
    email = Column("email", String(255), nullable=False, unique=True)
    senha = Column("senha", String(255), nullable=False)

    def __init__(self, nome, email, senha=None):
        self.nome = nome
        self.email = email
        self.senha = Hasher().hasherpswd(senha) if senha else None

    def __str__(self):
        return f"User(id={self.id}, nome='{self.nome}', email='{self.email}')"


class Cliente_Produto(Base):
    __tablename__ = "cliente_produto"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
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
    activate = Column("activate", Boolean, nullable=False, server_default="1")
    data_modificacao = Column("data_modificacao", TIMESTAMP, server_default=func.now())

    def __init__(self, cliente, valor):
        self.id_cliente = cliente.id
        self.valor = valor
        self.data_modificacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Carrinho(Base):
    __tablename__ = "carrinho"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("id_cliente", ForeignKey("clientes.id"), nullable=False)
    id_produto = Column("id_produto", ForeignKey("produtos.id"), nullable=False)
    quantidade = Column("quantidade", DECIMAL(15, 2), nullable=False)
    data = Column("data", TIMESTAMP, server_default=func.now())

    def __init__(self, id_cliente, id_produto, quantidade):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade = quantidade


def initialize_database():
    with DatabaseHandler() as database_handler:
        # Criação das tabelas no banco de dados
        Base.metadata.create_all(database_handler.get_engine())
        Logger.info("[INFO] - Initialization database sucessfully - [INFO]")
        result = (
            database_handler.session.query(User)
            .filter_by(nome="Renan Rodrigues")
            .first()
        )
        if not result:
            user = User("Renan Rodrigues", configs["user"], "admin")
            database_handler.session.add(user)
            database_handler.session.commit()
            Logger.sucess(f"[INFO] User {user.nome} added successfully [INFO]")


if __name__ == "__main__":
    initialize_database()
