from src.models.entities.database import Cliente_Produto, DatabaseHandler
from src.models.repository.user_repository import UserRepository


def update_divida(cliente):
    cliente = UserRepository().select_user(cliente)
    with DatabaseHandler() as db:
        if cliente:
            db.session.query(Cliente_Produto).filter(
                Cliente_Produto.id_cliente == cliente.id
            ).delete()
            db.session.commit()
            return True
        return False
