from decimal import Decimal
from typing import Literal

from src.models.entities.database import (
    CustomerProduct,
    DatabaseHandler,
    Debt,
    Product,
)
from src.models.repository.user_repository import UserRepository


def select_debt_by_client(cliente, cpf=None):
    with UserRepository() as us:
        if cpf:
            cliente = us.select_user_cpf(cpf)
        else:
            cliente = us.select_user(cliente)
    with DatabaseHandler() as db:
        if cliente:
            divida = (
                db.session.query(Debt).filter(Debt.id_cliente == cliente.id).first()
            )
            if divida:
                print("Valor", divida.valor)
                print("Pago", divida.pago)
                print("Total - Pago", divida.valor - divida.pago)
                return divida.valor - divida.pago
    return 0


def delete_dividas(cliente):
    with UserRepository() as us:
        cliente = us.select_user(cliente)
    with DatabaseHandler() as db:
        if cliente:
            db.session.query(CustomerProduct).filter(
                CustomerProduct.id_cliente == cliente.id
            ).delete()
            db.session.query(Debt).filter(Debt.id_cliente == cliente.id).update(
                {"valor": 0, "pago": 0}
            )
            db.session.commit()
            return True
        return False


def update_dividas(cliente, action: Literal["add", "remove"], valor=0):
    with UserRepository() as us:
        cliente = us.select_user(
            cliente,
        )
    with DatabaseHandler() as db:
        if cliente:
            if action == "add":
                clientes = (
                    db.session.query(CustomerProduct)
                    .filter(CustomerProduct.id_cliente == cliente.id)
                    .all()
                )
                total = sum([c.total for c in clientes])
                divida = (
                    db.session.query(Debt).filter(Debt.id_cliente == cliente.id).first()
                )
                if divida:
                    divida.valor = total
                    db.session.commit()
                    return True
                divida = Debt(cliente, total)
                db.session.add(divida)
                db.session.commit()
                return True
            else:
                divida = (
                    db.session.query(Debt).filter(Debt.id_cliente == cliente.id).first()
                )
                if divida.valor == 0 or (divida.valor - divida.pago) < valor:
                    return False
                if divida.valor == valor:
                    delete_dividas(cliente)
                    return True
                divida.pago += Decimal(valor)
                db.session.commit()
                return True
        return False


def register_sale(client, product, count: int = 0):
    with UserRepository() as us:
        user = us.select_user(client)
    if user:
        with DatabaseHandler() as db:
            product = db.session.query(Product).filter(Product.nome == product).first()
            if product:
                total = product.preco * count
                sale = CustomerProduct(
                    id_cliente=user.id,
                    id_produto=product.id,
                    preco=product.preco,
                    quantidade=count,
                    total=total,
                )
                divida = (
                    db.session.query(Debt).filter(Debt.id_cliente == user.id).first()
                )
                if divida:
                    divida.valor += total
                else:
                    divida = Debt(user, total)
                # remover do estoque
                product.estoque -= count
                db.session.add(sale)
                db.session.add(divida)
                db.session.commit()
                return True
    return False
