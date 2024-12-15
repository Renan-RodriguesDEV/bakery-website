from decimal import Decimal
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


# Função para selecionar o preço do produto pelo nome
def select_price_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute(
                "SELECT preco FROM produtos WHERE nome  like%s", (f"%{name}%",)
            )
            price = cursor.fetchone()
            return price


# Função para selecionar o cliente pelo nome
def select_cliente_id_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT id FROM clientes WHERE nome = %s", (name,))
            result = cursor.fetchall()
            return result[0]["id"] if result else None


def select_product_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute(
                "SELECT nome,preco,estoque FROM produtos WHERE nome like%s",
                (f"%{name}%",),
            )
            df = pd.DataFrame(cursor.fetchall(), columns=["nome", "preco", "estoque"])
            df.columns = ["Nome", "Preço", "Estoque"]
            return df


# Função para selecionar o estoque pelo nome do produto
def select_count_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT estoque FROM produtos WHERE nome = %s", (name,))
            df = pd.DataFrame(cursor.fetchall())
            return df


# Função para registrar um cliente
def register_client(name, cpf, telefone, email):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            sentence = "INSERT INTO clientes (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sentence,
                (name, cpf, telefone, email),
            )
            connective.commit()
            return True


# Função para registrar um produto
def register_product(name, price, count):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute(
                "INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)",
                (name, price, count),
            )
            connective.commit()
            return True


# Função para registrar um produto
def register_sale(cliente, produto, quantidade: int = 1):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            # Obter o ID do cliente pelo nome
            cursor.execute("SELECT id FROM clientes WHERE nome = %s", (cliente,))
            result_client = cursor.fetchone()
            if result_client:
                id_cliente = result_client["id"]
            else:
                raise ValueError(f"Cliente '{cliente}' não encontrado.")

            cursor.execute("SELECT id, preco FROM produtos WHERE nome = %s", (produto,))
            result_product = cursor.fetchone()
            if result_product:
                id_produto = result_product["id"]
                preco = result_product["preco"]
            else:
                raise ValueError(f"Produto '{produto}' não encontrado.")

            # Verificar se o cliente já possui o produto registrado
            cursor.execute(
                "SELECT quantidade FROM cliente_produto WHERE id_cliente = %s AND id_produto = %s",
                (id_cliente, id_produto),
            )
            existing_record = cursor.fetchone()

            total = preco * quantidade

            if existing_record:
                # Atualizar a quantidade e o total do produto
                nova_quantidade = existing_record["quantidade"] + quantidade
                novo_total = preco * nova_quantidade
                cursor.execute(
                    "UPDATE cliente_produto SET quantidade = %s, total = %s WHERE id_cliente = %s AND id_produto = %s",
                    (nova_quantidade, novo_total, id_cliente, id_produto),
                )
                connective.commit()
                return True

            # Inserir novo registro com total
            query = """
            INSERT INTO cliente_produto (id_cliente, id_produto, preco, quantidade, total) 
            VALUES (%s, %s, %s, %s, %s)
            """
            rows = cursor.execute(
                query, (id_cliente, id_produto, preco, quantidade, total)
            )
            connective.commit()
            return True if rows > 0 else False


def update_divida(cliente):
    result = select_cliente_id_by_name(cliente)
    if result:
        connective = pymysql.connect(**db_data)
        with connective as connective:
            with connective.cursor() as cursor:
                query = "DELETE FROM cliente_produto WHERE id_cliente = %s"
                cursor.execute(query, (result))
                connective.commit()
                return True
    return False


# Função para consultar a dívida do cliente
def select_debt_by_client(cliente, cpf=None):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            if cpf:
                query = """
                    SELECT c.nome, SUM(cp.total) AS divida_total
                    FROM cliente_produto cp 
                    JOIN clientes c ON cp.id_cliente = c.id
                    WHERE c.nome = %s AND c.cpf = %s
                    """
                cursor.execute(query, (cliente, cpf))
            else:
                query = """
                SELECT c.nome, SUM(cp.total) AS divida_total
                FROM cliente_produto cp 
                JOIN clientes c ON cp.id_cliente = c.id
                WHERE c.nome = %s
                """
                cursor.execute(query, (cliente,))
            data = cursor.fetchall()
            return data[0].get("divida_total") if data else 0.00


def select_user(name, passwd):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = "SELECT * FROM users WHERE nome = %s AND senha = %s"
            cursor.execute(query, (name, passwd))
            result = cursor.fetchone()
            if result:
                senha = result["senha"]
                usuario = result["nome"]
                return {"username": usuario, "password": senha}
            return {"username": "", "password": ""}


def select_user_client(name, passwd):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = "SELECT * FROM clientes WHERE nome = %s AND cpf = %s"
            cursor.execute(query, (name, passwd))
            result = cursor.fetchone()
            if result:
                senha = result["cpf"]
                usuario = result["nome"]
                return {"username": usuario, "password": senha}
            return {"username": "", "password": ""}


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


def delete_product(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            try:
                query = "DELETE FROM produtos WHERE nome = %s"
                cursor.execute(query, (name,))
                connective.commit()
                return True
            except Exception as e:
                return False


def delete_client(cliente):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            try:
                query = "DELETE FROM clientes WHERE nome = %s"
                cursor.execute(query, (cliente,))
                connective.commit()
                return True
            except Exception as e:
                return False


# Teste básico
if __name__ == "__main__":
    df = select_debt_by_client("Renan de Souza Rodrigues")
    print(df)
