import streamlit as st

from src.models.repository.user_repository import UserRepository
from src.models.repository.cart_repository import CartRepository
from src.models.repository.product_repository import ProductRepository
from src.controller.payments import payment
from src.models.repository.dataframes_repository import (
    select_all_produtos,
)
from src.utils.uteis import Logger


# Função para realizar a compra
def realizar_compra():
    st.title("Realizar Compra")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_produtos = select_all_produtos()
    cliente_session = st.session_state["username"]
    st.write(f"Cliente: {cliente_session}")
    produto = st.selectbox("Selecione o produto", df_produtos)
    preco = ProductRepository().select_product_price(produto)
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    col1, col2 = st.columns([1, 1])

    if produto and preco:
        col1.html(
            f"""
            <p><span style='color: cyan'>Produto: </span><strong>{produto}</strong></p>
            <p><span style='color: cyan;'>Preço Unitário: </span><strong>R$ {preco}</strong></p>
            <p><span style='color: cyan;'>Valor Final: </span><strong>R$ {preco*quantidade}</strong></p>
            """
        )
        disable = True
        if col1.button("Adicionar ao carrinho", type="primary"):
            cliente_obj = UserRepository().select_user(cliente_session, "Client")
            produto_obj = ProductRepository().select_product(produto)
            Logger.info(f"produto: {produto_obj}")
            Logger.info(f"cliente: {cliente_obj}")
            if produto_obj and cliente_obj:
                with CartRepository() as cart_repository:
                    cart_repository.add_to_cart(cliente_obj, produto_obj, quantidade)
                st.success(f" +{quantidade} {produto} adicionado ao carrinho 🛒")
                st.success(f" +{preco*quantidade} adicionado ao valor do carrinho 💵")
                disable = False
            else:
                st.error("Erro ao adicionar ao carrinho")
        if st.button("Ir para o carrinho", disabled=disable):
            st.session_state["pagina"] = "cart"
            st.rerun()
     

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
