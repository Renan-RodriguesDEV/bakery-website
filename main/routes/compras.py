import streamlit as st

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
    cliente = st.session_state["usuario"]
    st.write(f"Cliente: {cliente}")
    produto = st.selectbox("Selecione o produto", df_produtos)
    preco = ProductRepository().select_product_price(produto)
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    if produto and preco:
        st.markdown(
            f"""
            \n:green[PRODUTO]: **{produto}** 
            \n:green[PREÇO UNITÁRIO]: **`R$`{preco}** 
            \n:green[VALOR FINAL]: **`R$`{preco*quantidade}**""",
            unsafe_allow_html=True,
        )
        if st.button("Comprar", type="primary"):
            try:
                link_paryment = payment(str(produto), float(preco), int(quantidade))
                Logger.log_blue(f"link para pagamento {link_paryment}")
                # Redireciona automaticamente
                st.page_link(
                    page=link_paryment, label=":green[Ir para o Pagamento]", icon="💸"
                )

                st.success(
                    f"Venda registrada com sucesso no valor de {preco*quantidade}!"
                )
            except Exception as e:
                st.error("Erro ao registrar a venda")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
