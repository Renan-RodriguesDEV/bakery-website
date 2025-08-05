import pandas as pd
from sqlalchemy import text
from src.models.entities.connection_handler import get_db_session
from src.utils.uteis import Logger


# Função para selecionar todos os produtos
def select_all_products():
    with get_db_session() as session:
        query = text("SELECT nome, preco, estoque FROM produtos ORDER BY nome")
        result = session.execute(query)

        # Converte para lista de dicionários
        data = [dict(row._mapping) for row in result]

        if not data:
            return pd.DataFrame(columns=["Nome", "Preço", "Estoque"])

        df = pd.DataFrame(data)
        df.columns = ["Nome", "Preço", "Estoque"]
        return df


def search_product(name):
    with get_db_session() as session:
        query = text("SELECT * FROM produtos WHERE nome LIKE :name ORDER BY nome")
        result = session.execute(query, {"name": f"%{name}%"})

        # Converte para lista de dicionários
        data = [dict(row._mapping) for row in result]

        if not data:
            return pd.DataFrame(columns=["id", "nome", "preco", "estoque", "categoria"])

        return pd.DataFrame(data)


# Função para selecionar todos os clientes
def select_all_clientes():
    try:
        with get_db_session() as session:
            query = text(
                "SELECT nome, cpf, telefone, email FROM clientes ORDER BY nome"
            )
            result = session.execute(query)

            # Converte para lista de dicionários
            data = [dict(row._mapping) for row in result]

            Logger.info(f"Dados retornados: {data}")

            if not data:
                return pd.DataFrame(columns=["nome", "cpf", "telefone", "email"])

            return pd.DataFrame(data)

    except Exception as e:
        Logger.error(f"Erro ao selecionar clientes: {e}")
        return pd.DataFrame(columns=["nome", "cpf", "telefone", "email"])


# Função para selecionar o estoque pelo nome do produto
def select_count_by_name(name):
    with get_db_session() as session:
        query = text("SELECT estoque FROM produtos WHERE nome = :name")
        result = session.execute(query, {"name": name})

        # Converte para lista de dicionários
        data = [dict(row._mapping) for row in result]

        if not data:
            return pd.DataFrame(columns=["estoque"])

        return pd.DataFrame(data)


def select_all_sales_by_client(client_name=None, cpf=None, client_email=None):
    with get_db_session() as session:
        base_query = """
            SELECT c.nome, p.nome AS produto, cp.preco AS preco, cp.quantidade AS quantidade, cp.total AS total, cp.data AS data
            FROM cliente_produto cp 
            JOIN clientes c ON cp.id_cliente = c.id
            JOIN produtos p ON cp.id_produto = p.id
            WHERE {} ORDER BY cp.data DESC
        """

        params = {}

        if client_email:
            if cpf:
                query_text = base_query.format("c.email = :email OR c.cpf = :cpf")
                params = {"email": client_email, "cpf": cpf}
            else:
                query_text = base_query.format("c.email = :email")
                params = {"email": client_email}
        elif client_name:
            if cpf:
                query_text = base_query.format("c.nome = :nome OR c.cpf = :cpf")
                params = {"nome": client_name, "cpf": cpf}
            else:
                query_text = base_query.format("c.nome = :nome")
                params = {"nome": client_name}
        else:
            return None

        Logger.warning(f"Query executada: {query_text}")

        query = text(query_text)
        result = session.execute(query, params)

        # Converte para lista de dicionários
        data = [dict(row._mapping) for row in result]

        if not data:
            return pd.DataFrame(
                columns=["nome", "produto", "preco", "quantidade", "total", "data"]
            )

        return pd.DataFrame(data)


# Função para selecionar todos os produtos por categoria
def select_all_products_by_category(category):
    with get_db_session() as session:
        query = text("""
            SELECT nome, preco, estoque
            FROM produtos
            WHERE categoria = :categoria ORDER BY nome
        """)

        result = session.execute(query, {"categoria": category})

        # Converte para lista de dicionários
        data = [dict(row._mapping) for row in result]

        if not data:
            return pd.DataFrame(columns=["Nome", "Preço", "Estoque"])

        df = pd.DataFrame(data)
        df.columns = ["Nome", "Preço", "Estoque"]
        return df
