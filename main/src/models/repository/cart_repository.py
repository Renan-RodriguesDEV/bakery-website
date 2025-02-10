from src.models.entities.database import DatabaseHandler, Carrinho, Produto


class CartRepository(DatabaseHandler):
    def add_to_cart(self, user, product, count):
        with self:
            carrinho = Carrinho(
                id_cliente=user.id, id_produto=product.id, quantidade=count
            )
            self.session.add(carrinho)
            self.session.commit()
            return True
        return False

    def get_cart_by_user(self, user_id):
        with self:
            carrinhos = (
                self.session.query(Carrinho)
                .filter(Carrinho.id_cliente == user_id)
                .all()
            )
            return carrinhos

    def remove_from_cart(self, user_id, product_id):
        with self:
            carrinho = (
                self.session.query(Carrinho)
                .filter(
                    Carrinho.id_cliente == user_id, Carrinho.id_produto == product_id
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
                self.session.query(Carrinho)
                .filter(
                    Carrinho.id_cliente == user_id, Carrinho.id_produto == product_id
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
            product = self.session.query(Produto).filter(Produto.id == product).first()
            product.estoque -= count
            self.session.commit()
            return True
        return False
