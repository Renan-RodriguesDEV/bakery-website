import pandas as pd
import psycopg2
import psycopg2.extras
from src.models.entities.connection_handler import get_connection
from src.utils.uteis import Logger


# Função para selecionar todos os produtos
def select_all_products():
    connective = get_connection()
    with connective as connective:
        with connective.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT nome,preco,estoque FROM produtos ORDER BY nome ")
            df = pd.DataFrame(cursor.fetchall(), columns=["nome", "preco", "estoque"])
            df.columns = ["Nome", "Preço", "Estoque"]
            return df


def search_product(name):
    connective = get_connection()
    with connective as connective:
        with connective.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM produtos WHERE nome LIKE%s ORDER BY nome", (f"%{name}%",)
            )
            data = cursor.fetchall()
            return data if data else None


# Função para selecionar todos os clientes
def select_all_clientes():
    connective = get_connection()
    with connective as connective:
        with connective.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT nome,cpf,telefone,email FROM clientes ORDER BY nome")
            df = pd.DataFrame(cursor.fetchall(), columns=["nome"])
            return df


# Função para selecionar o estoque pelo nome do produto
def select_count_by_name(name):
    connective = get_connection()
    with connective as connective:
        with connective.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT estoque FROM produtos WHERE nome = %s", (name,))
            df = pd.DataFrame(cursor.fetchall())
            return df


def select_all_sales_by_client(client_name=None, cpf=None, client_email=None):
    connective = get_connection()
    with connective as connective:
        with connective.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # Base da query
            base_query = """
                SELECT c.nome, p.nome AS produto, cp.preco, cp.quantidade, cp.total, cp.data
                FROM cliente_produto cp 
                JOIN clientes c ON cp.id_cliente = c.id
                JOIN produtos p ON cp.id_produto = p.id
                WHERE {} ORDER BY cp.data DESC
            """

            # Define condições e parâmetros baseado nos argumentos fornecidos
            if client_email:
                if cpf:
                    query = base_query.format("c.email = %s OR c.cpf = %s")
                    cursor.execute(query, (client_email, cpf))
                else:
                    query = base_query.format("c.email = %s")
                    cursor.execute(query, (client_email,))
            elif client_name:
                if cpf:
                    query = base_query.format("c.nome = %s OR c.cpf = %s")
                    cursor.execute(query, (client_name, cpf))
                else:
                    query = base_query.format("c.nome = %s")
                    cursor.execute(query, (client_name,))
            else:
                return None

            Logger.warning(f"Query executada: {query}")
            data = cursor.fetchall()
            return pd.DataFrame(data) if data else None


# Função para selecionar todos os produtos por categoria
def select_all_products_by_category(category):
    connective = get_connection()
    with connective as connective:
        with connective.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """
                SELECT nome, preco, estoque
                FROM produtos
                WHERE categoria = %s ORDER BY nome
            """
            cursor.execute(query, (category,))
            data = cursor.fetchall()
            if not data:
                return pd.DataFrame(columns=["Nome", "Preço", "Estoque"])
            df = pd.DataFrame(data)
            df.columns = ["Nome", "Preço", "Estoque"]
            return df
