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
            with open(backup_file, "w") as f:
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
