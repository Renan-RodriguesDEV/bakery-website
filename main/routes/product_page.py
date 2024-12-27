import io

import streamlit as st
from pandas import DataFrame
from src.models.repository.dividas_repository import (
    delete_dividas,
    register_sale,
    select_debt_by_client,
    update_dividas,
)
from src.models.repository.product_repository import ProductRepository
from src.utils.uteis import Logger

from src.models.repository.dataframes_repository import (
    select_all_clientes,
    select_all_produtos,
    select_all_sales_by_client,
)


def consulta_produto():
    """Pagina para consulta de produtos"""
    st.title("Consulta de Produtos")
    produtos = select_all_produtos()
    flag = True if produtos.empty else False
    # Aqui você poderia listar os produtos cadastrados. Exemplo simples:
    st.table(produtos)
    nome = st.text_input("Digite o nome do produto para consultar")
    produto = ProductRepository().select_product(nome)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Consultar", type="primary"):
            if produto:
                st.table(
                    {
                        "Produto": {
                            "Nome": produto.nome,
                            "Preço": produto.preco,
                            "Estoque": produto.estoque,
                        }
                    }
                )
            else:
                st.error("Nenhum produto encontrado com esse nome")

    @st.cache_data
    def converter_df_to_excel(dataframe: DataFrame):
        buffer = io.BytesIO()
        dataframe.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer

    with col2:
        st.download_button(
            "Download produtos",
            data=converter_df_to_excel(produtos),
            file_name="produtos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            disabled=flag,
        )
    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de dívida de clientes
def consulta_divida():
    """Pagina para a consulta de dívida de clientes"""

    @st.cache_data
    def converter_df_to_excel(dataframe: DataFrame):
        try:
            buffer = io.BytesIO()
            dataframe.to_excel(buffer, index=False)
            buffer.seek(0)
            return buffer
        except Exception as e:
            Logger.error(str(e))

    if st.session_state["owner"]:
        st.title("Consulta de Dívida de Clientes")
        # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
        df_clientes = select_all_clientes()
        cliente = st.selectbox(
            "Selecione o cliente",
            df_clientes["nome"].to_list(),
        )
        divida = select_debt_by_client(
            cliente,
        )
        st.subheader(f"Divida do cliente :gray[{cliente}]", divider="red")
        st.write(
            f"""<p style="font-size:30px;">Valor atual: <span style="text-decoration:underline; color:green; font-weight:bold;">R$ {divida if divida else 0.00}</span></p>""",
            unsafe_allow_html=True,
        )

        if st.button("Consulta completa", type="primary"):
            st.table(select_all_sales_by_client(cliente))
        try:
            st.download_button(
                label="Download divida",
                data=converter_df_to_excel(select_all_sales_by_client(cliente)),
                file_name="divida.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
            )
        except Exception as e:
            st.warning(f"Não dividas existentes para o cliente {cliente}")
            st.button(f"Dowload divida", disabled=True)
            Logger.error(str(e))
        if st.button("Voltar"):
            st.session_state["pagina"] = "homepage"
            st.rerun()
    else:
        st.title("Consulta de Dívida de Clientes")

        with st.form(key="consulta_form"):
            cliente = st.text_input(
                "Nome completo", help="Digite o nome completo como no cadastro"
            )
            cpf = st.text_input(
                "CPF",
                help="Digite seu cpf completo como no cadastro, sem caracteres",
                max_chars=11,
                placeholder="123.456.789-00",
            )
            consultar = st.form_submit_button("Consultar")

        if consultar:
            divida = select_debt_by_client(cliente, cpf)
            st.write(f"Divida do cliente {cliente}: R$ {divida if divida else 0.00}")
            divida_total = select_all_sales_by_client(cliente)
            if not divida_total.empty:
                st.table(divida_total)
                st.download_button(
                    label="Download divida",
                    data=converter_df_to_excel(select_all_sales_by_client(cliente)),
                    file_name="divida.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.error("Nenhuma divida encontrado !!!")

        if st.button("Voltar"):
            st.session_state["pagina"] = "homepage"
            st.rerun()


def atualizar_divida():
    """Pagina para atualizar a dívida de clientes"""
    st.title("Atualizar Dívida de Clientes")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_clientes = select_all_clientes()
    df_produtos = select_all_produtos()
    cliente = st.selectbox("Selecione o cliente", df_clientes["nome"].to_list())
    action = st.selectbox("Adicionar/Remover divida", ["Adicionar", "Remover"])
    if action == "Adicionar":
        if df_produtos.empty:
            st.error("Nenhum produto cadastrado")
            produto = None
        else:
            produto = st.selectbox("Selecione o produto", df_produtos)
        if df_clientes.empty:
            st.error("Nenhum cliente cadastrado")
        preco = None
        try:
            if produto:
                preco = ProductRepository().select_product_price(produto)
        except Exception as e:
            st.warning("Produto não encontrado")
            Logger.error(str(e))
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        st.markdown(
            f"<span style='font-size:30px; text-decoration:underline; font-family:JetBrains mono'>Valor final: :green[${preco * quantidade if (preco and quantidade)!=None else 0}]</span>",
            unsafe_allow_html=True,
        )
        if st.button("Atualizar", type="primary", disabled=df_produtos.empty):

            is_register = register_sale(cliente, produto, quantidade)
            if is_register:
                st.success(
                    f"Venda registrada com sucesso no valor de R${preco*quantidade}!"
                )
            else:
                st.error("Erro ao registrar a venda")
    else:
        divida_total = select_debt_by_client(cliente)
        st.write(
            f"**O cliente :blue[{cliente}] tem a divida total no valor: :gray[R${divida_total}]**"
        )
        valor_remover = st.number_input(
            "Valor a ser removido", min_value=0.0, step=0.01
        )
        is_pag = None
        st.warning("Cuidado ao remover a divida, essa ação não pode ser desfeita")
        col1, col2 = st.columns([1, 1])
        if col1.button(f"Remover Valor R${valor_remover}", type="primary"):
            is_pag = update_dividas(cliente, "remove", valor_remover)
            if valor_remover > divida_total or valor_remover < 0:
                st.error(
                    "Insira valores positivos ao remover a divida e não insira valores maiores que a divida!!!"
                )
        if col2.button(
            "Zerar divida",
            type="primary",
            help="Atenção, essa ação não pode ser desfeita",
        ):
            is_pag = delete_dividas(cliente)
        if is_pag is not None and is_pag:
            st.success(
                f"Pagamento registrado com sucesso!! a conta atual está em R$ {select_debt_by_client(cliente)}"
            )
        elif is_pag is None or not is_pag:
            st.warning("Aguardando efetuação de pagamento")
        else:
            st.error("Erro ao registrar a pagamento")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
