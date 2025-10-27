import datetime
from pathlib import Path

from sqlalchemy import text

from src.models.entities.connection_handler import get_db_session


def backup_with_psycopg2():
    BACKUP_DIR = Path("backups")
    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"neon_backup_{timestamp}.sql"

    try:
        # Conectar ao banco
        with get_db_session() as session:
            # Obter lista de tabelas
            tables = session.execute(
                text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            ).fetchall()

            # Criar backup comprimido
            with open(backup_file, "w", encoding="utf-8") as f:
                for table in tables:
                    table_name = table[0]

                    # Dump da estrutura da tabela
                    session.execute(
                        text(f"""
                        SELECT 'CREATE TABLE ' || '{table_name}' || ' (' ||
                        string_agg(column_name || ' ' || data_type, ', ') || ');'
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}'
                    """)
                    ).fetchall()

                    # Dump dos dados
                    rows = session.execute(
                        text(f"SELECT * FROM {table_name}")
                    ).fetchall()

                    for row in rows:
                        # Escrever dados no arquivo
                        f.write(f"INSERT INTO {table_name} VALUES {row};\n")

            print(f"Backup criado: {backup_file}")
            return str(backup_file)

    except Exception as e:
        print(f"Erro: {e}")
        return None


def fix_id_serial():
    """Comando SQL pra deixar o id sequencial em todas as tabelas.

    Sincroniza a SEQUENCE com o MAX(id) de cada tabela.
    O comando setval() garante que o PRÓXIMO ID seja maior que o maior ID existente.
    """
    query = """
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM users;
SELECT setval(pg_get_serial_sequence('clientes', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM clientes;
SELECT setval(pg_get_serial_sequence('produtos', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM produtos;
SELECT setval(pg_get_serial_sequence('cliente_produto', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM cliente_produto;
SELECT setval(pg_get_serial_sequence('carrinho', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM carrinho;
SELECT setval(pg_get_serial_sequence('dividas', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM dividas;
SELECT setval(pg_get_serial_sequence('notifications', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM notifications;"""
    try:
        with get_db_session() as session:
            session.execute(text(query))
            session.commit()
    except Exception as e:
        print(f"Erro ao corrigir IDs sequenciais: {e}")
        return False
    print("IDs sequenciais corrigidos com sucesso.")
    return True
