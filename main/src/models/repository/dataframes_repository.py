import pymysql
import pandas as pd


db_data = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "db_comercio",
    "cursorclass": pymysql.cursors.DictCursor,
}


# Função para selecionar todos os produtos
def select_all_produtos():
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT nome,preco,estoque FROM produtos")
            df = pd.DataFrame(cursor.fetchall(), columns=["nome", "preco", "estoque"])
            df.columns = ["Nome", "Preço", "Estoque"]
            return df


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
