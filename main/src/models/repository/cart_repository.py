from src.models.entities.database import DatabaseHandler, Product, ShoppingCart


class CartRepository(DatabaseHandler):
    def add_to_cart(self, user, product, count):
        with self:
            carrinho = ShoppingCart(
                id_cliente=user.id, id_produto=product.id, quantidade=count
            )
            self.session.add(carrinho)
            self.session.commit()
            return True
        return False

    def get_cart_by_user(self, user_id):
        with self:
            carrinhos = (
                self.session.query(ShoppingCart)
                .filter(ShoppingCart.id_cliente == user_id)
                .all()
            )
            return carrinhos

    def remove_from_cart(self, user_id, product_id):
        with self:
            carrinho = (
                self.session.query(ShoppingCart)
                .filter(
                    ShoppingCart.id_cliente == user_id,
                    ShoppingCart.id_produto == product_id,
                )
                .first()
            )
            self.session.delete(carrinho)
            self.session.commit()
            return True
        return False

    def remove_all_from_cart(self, user_id, product_id):
        with self:
            carrinhos = (
                self.session.query(ShoppingCart)
                .filter(
                    ShoppingCart.id_cliente == user_id,
                    ShoppingCart.id_produto == product_id,
                )
                .all()
            )
            for carrinho in carrinhos:
                self.session.delete(carrinho)
                self.session.commit()
            return True
        return False

    def remove_from_stoke(self, product, count):
        with self:
            product = self.session.query(Product).filter(Product.id == product).first()
            product.estoque -= count
            self.session.commit()
            return True
        return False
