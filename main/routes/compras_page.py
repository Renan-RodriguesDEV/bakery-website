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
    col1, col2 = st.columns([1, 1])

    if produto and preco:
        col1.html(
            f"""
            <p><span style='color: cyan'>Produto: </span><strong>{produto}</strong></p>
            <p><span style='color: cyan;'>Preço Unitário: </span><strong>R$ {preco}</strong></p>
            <p><span style='color: cyan;'>Valor Final: </span><strong>R$ {preco*quantidade}</strong></p>
            """
        )
        if col1.button("Comprar", type="primary"):
            try:
                link_paryment = payment(str(produto), float(preco), int(quantidade))
                Logger.sucess(f"link para pagamento {link_paryment}")
                # Redireciona automaticamente
                st.page_link(
                    page=link_paryment, label=":green[Ir para o Pagamento]", icon="💸"
                )

                st.success(
                    f"Venda registrada com sucesso no valor de {preco*quantidade}!"
                )
            except Exception as e:
                st.error("Erro ao registrar a venda")
        col2.html(
            """
<h4>Se preferir pague em pix 🪙</h4> 
<p><b>Proprietario: </b> <span style='text-decoration: underline;'>Renan Rodrigues</span></p>
<p>Chave:</p>"""
        )
        col2.code("(19) 99872-2472")
        col2.html("<h4/>Banco Santander (SA)</h4>")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
