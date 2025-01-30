import streamlit as st
from src.models.repository.cart_repository import CartRepository
from src.models.repository.product_repository import ProductRepository
from src.models.repository.user_repository import UserRepository


def shopping_cart():
    product_repository = ProductRepository()
    cart_repository = CartRepository()
    user_repository = UserRepository()
    user_session = st.session_state["username"]
    st.title(f"Bem vindo ao seu carrinho de compras {user_session}")
    st.subheader("")
    st.selectbox(
        "Itens no carrinho!!!",
        [
            carrinho.id_produto
            for carrinho in cart_repository.get_cart_by_user(
                user_repository.select_user(user_session, "Client").id
            )
        ],
    )
    if st.button("Ir para home"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
