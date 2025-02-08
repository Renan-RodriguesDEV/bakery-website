import streamlit as st

from src.models.repository.user_repository import UserRepository
from src.models.repository.cart_repository import CartRepository
from src.models.repository.product_repository import ProductRepository
from src.models.repository.dataframes_repository import (
    select_all_products,
    select_all_products_by_category,
)
from src.utils.uteis import Logger


# Função para realizar a compra
def realizar_compra():
    st.title(":green[Faça sua(s) Compra(s) 🛒]")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_produtos = select_all_products()
    cliente_session = st.session_state["username"]
    st.write(f"Cliente: {cliente_session}")
    categoria = st.selectbox(
        "Selecione uma da(s) categoria(s)",
        ["categoria", "Bebidas", "Doces", "Salgados", "Padaria", "Mercearia"],
    )
    print(categoria)
    produto = st.selectbox(
        "Selecione o produto",
        (
            df_produtos
            if not categoria or categoria == "categoria"
            else select_all_products_by_category(categoria)
        ),
    )
    preco = ProductRepository().select_product_price(produto)
    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        step=1,
        max_value=ProductRepository().select_product(produto).estoque,
    )

    col1, col2 = st.columns([1, 1])

    if produto and preco:
        with st.container():
            st.markdown(
                f"""
                <div style='background-color: #262730; padding: 10px; border-radius: 5px; width: 100%;font-size:18px'>
                <p style='color: white; display: flex; justify-content: space-between;'><span style='color: #ff4b4b'>Produto: </span><strong>{produto}</strong></p>
                <p style='color: white; display: flex; justify-content: space-between;'><span style='color: #ff4b4b'>Preço Unitário: </span><strong>R$ {preco}</strong></p>
                <p style='color: white; display: flex; justify-content: space-between;'><span style='color: #ff4b4b'>Valor Final: </span><strong>R$ {preco*quantidade}</strong></p>
                </div>
                <br/>
                """,
                unsafe_allow_html=True,
            )
        disable = True
        if col1.button("Adicionar ao carrinho", type="primary"):
            cliente_obj = UserRepository().select_user(cliente_session, "Cliente")
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
