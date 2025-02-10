import pymysql
import pandas as pd
from src.utils.uteis import Logger
from src.models.configs.config_db import configs_db


db_data = {
    "host": configs_db["host"],
    "user": configs_db["username"],
    "password": configs_db["password"],
    "database": configs_db["database"],
    "cursorclass": pymysql.cursors.DictCursor,
}

Logger.info(db_data)


# Função para selecionar todos os produtos
def select_all_products():
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT nome,preco,estoque FROM produtos")
            df = pd.DataFrame(cursor.fetchall(), columns=["nome", "preco", "estoque"])
            df.columns = ["Nome", "Preço", "Estoque"]
            return df


def search_product(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos WHERE nome LIKE%s", (f"%{name}%",))
            data = cursor.fetchall()
            return data if data else None


# Função para selecionar todos os clientes
def select_all_clientes():
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT nome,cpf,telefone,email FROM clientes")
            df = pd.DataFrame(cursor.fetchall(), columns=["nome"])
            return df


# Função para selecionar o estoque pelo nome do produto
def select_count_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT estoque FROM produtos WHERE nome = %s", (name,))
            df = pd.DataFrame(cursor.fetchall())
            return df


def select_all_sales_by_client(client_name=None, cpf=None, client_email=None):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = f"""
                SELECT c.nome, p.nome AS produto, cp.preco, cp.quantidade, cp.total, cp.data
                FROM cliente_produto cp 
                JOIN clientes c ON cp.id_cliente = c.id
                JOIN produtos p ON cp.id_produto = p.id
                WHERE {'c.nome = %s' if client_name else 'c.email = %s'}  {'OR c.cpf = %s' if cpf else ''}
            """
            Logger.warning(f"{query} , ({client_name},{cpf})")
            if cpf:
                cursor.execute(query, (client_name, cpf))
                Logger.warning(f"{query} , ({client_name},{cpf})")
            else:
                cursor.execute(query, (client_name,))
                Logger.warning(f"{query} , ({client_name})")

            data = cursor.fetchall()
            return pd.DataFrame(data) if data else None


# Função para selecionar todos os produtos por categoria
def select_all_products_by_category(category):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = """
                SELECT nome, preco, estoque
                FROM produtos
                WHERE categoria = %s
            """
            cursor.execute(query, (category,))
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            df.columns = ["Nome", "Preço", "Estoque"]
            return df if data else None
