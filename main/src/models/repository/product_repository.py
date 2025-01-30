from ..entities.database import DatabaseHandler, Produto
from ...utils.uteis import Logger


class ProductRepository(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def insert_product(self, name, price, stock):
        with self:
            product = Produto(nome=name, preco=price, estoque=stock)
            self.session.add(product)
            self.session.commit()
            return True

    def select_product(self, name):
        with self:
            product = (
                self.session.query(Produto)
                .filter(Produto.nome.like(f"%{name}%"))
                .first()
            )
            return product

    def select_product_by_id(self, id):
        with self:
            product = self.session.query(Produto).filter(Produto.id == id).first()
            return product

    def select_product_price(self, nome):
        with self:
            product = self.session.query(Produto).filter_by(nome=nome).first()
            return product.preco if product else None

    def select_all_products(self):
        with self:
            products = self.session.query(Produto).all()
            return products

    def update_product_price(self, name, new_price):
        with self:
            try:
                product = self.session.query(Produto).filter_by(nome=name).first()
                product.preco = new_price
                self.session.commit()
                return True
            except Exception as e:
                Logger.error(e)
                return False

    def update_product_stock(self, name, new_stock):
        with self:
            try:
                product = self.session.query(Produto).filter_by(nome=name).first()
                product.estoque = new_stock
                self.session.commit()
                return True
            except Exception as e:
                Logger.error(e)
                return False

    def delete_product(self, name):
        with self:
            try:
                product = self.session.query(Produto).filter_by(nome=name).first()
                self.session.delete(product)
                self.session.commit()
                return True
            except Exception as e:
                Logger.error(e)
                return False
