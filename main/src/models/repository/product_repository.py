from ...utils.uteis import Logger
from ..entities.database import DatabaseHandler, Product


class ProductRepository(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def insert_product(self, name, price, stock, category):
        with self:
            product = Product(nome=name, preco=price, estoque=stock, categoria=category)
            self.session.add(product)
            self.session.commit()
            return True

    def select_product(self, name):
        with self:
            product = (
                self.session.query(Product)
                .filter(Product.nome.like(f"%{name}%"))
                .first()
            )
            return product

    def select_product_by_id(self, id):
        with self:
            product = self.session.query(Product).filter(Product.id == id).first()
            return product

    def select_product_price(self, nome):
        with self:
            product = self.session.query(Product).filter_by(nome=nome).first()
            return product.preco if product else None

    def select_all_products(self):
        with self:
            products = self.session.query(Product).all()
            return products

    def update_product_price(self, name, new_price):
        with self:
            try:
                product = self.session.query(Product).filter_by(nome=name).first()
                product.preco = new_price
                self.session.commit()
                self.session.refresh(product)
                return True
            except Exception as e:
                Logger.error(e)
                return False

    def update_product_stock(self, name, new_stock):
        with self:
            try:
                product = self.session.query(Product).filter_by(nome=name).first()
                product.estoque = new_stock
                self.session.commit()
                self.session.refresh(product)
                return True
            except Exception as e:
                Logger.error(e)
                return False

    def delete_product(self, name):
        with self:
            try:
                product = self.session.query(Product).filter_by(nome=name).first()
                self.session.delete(product)
                self.session.commit()
                return True
            except Exception as e:
                Logger.error(e)
                return False
