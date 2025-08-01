import sys

from main.src.models.entities.database import initialize_database

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "initdb":
        initialize_database()
        print("Banco de dados criado com sucesso!")
    else:
        print("Comando não reconhecido. Use 'initdb'.")
