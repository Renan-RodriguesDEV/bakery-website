import pymysql
import pandas as pd
from streamlit import secrets

_USERNAME = secrets["TEST_USER_DB"]
_PASSWORD = secrets["TEST_PASSWORD_DB"]
_HOST = secrets["TEST_HOST_DB"]
_DATABASE = secrets["TEST_DATABASE_NAME"]

db_data = {
    "host": _HOST,
    "user": _USERNAME,
    "password": _PASSWORD,
    "database": _DATABASE,
    "cursorclass": pymysql.cursors.DictCursor,
}

print(db_data)


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


def select_all_sales_by_client(cliente):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = """
                SELECT c.nome, p.nome AS produto, cp.preco, cp.quantidade, cp.total, cp.data
                FROM cliente_produto cp 
                JOIN clientes c ON cp.id_cliente = c.id
                JOIN produtos p ON cp.id_produto = p.id
                WHERE c.nome = %s
            """
            cursor.execute(query, (cliente,))
            data = cursor.fetchall()
            return pd.DataFrame(data) if data else None


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
