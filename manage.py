import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "main"))
from main.src.models.entities.database import initialize_database
from main.src.utils.migrations import backup_with_psycopg2, fix_id_serial

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        os.system("streamlit run main/app.py")
    elif len(sys.argv) > 1 and sys.argv[1] == "initdb":
        initialize_database()
        print("Banco de dados criado com sucesso!")
    elif len(sys.argv) > 1 and sys.argv[1] == "psql-dump":
        backup_with_psycopg2()
    elif len(sys.argv) > 1 and sys.argv[1] == "fix-id":
        fix_id_serial()
    else:
        print("Comando não reconhecido. Use 'initdb', 'psql-dump' e 'fix-id'.")
