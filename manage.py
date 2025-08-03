import sys

from main.src.models.entities.database import initialize_database
from main.src.utils.migrations import backup_with_psycopg2

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "initdb":
        initialize_database()
        print("Banco de dados criado com sucesso!")
    elif len(sys.argv) > 1 and sys.argv[1] == "psql-dump":
        backup_with_psycopg2()
    else:
        print("Comando não reconhecido. Use 'initdb'.")
