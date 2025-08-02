import io
from venv import logger

import streamlit as st
from pandas import DataFrame
from src.models.repository.dataframes_repository import (
    select_all_clientes,
    select_all_products,
    select_all_sales_by_client,
)
from src.models.repository.dividas_repository import (
    delete_dividas,
    register_sale,
    select_debt_by_client,
    update_dividas,
)
from src.models.repository.product_repository import ProductRepository
from src.utils.uteis import Logger, str_as_number


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
        df_clientes = select_all_clientes()
        if df_clientes.empty:
            st.subheader("Ops!! Houve algum erro no processo..")
            st.error("Nenhum cliente cadastrado")
            st.warning("Cadastre algum cliente antes de acessar está pagina")
            if st.sidebar.button(
                "ir para home", use_container_width=True, type="primary"
            ):
                st.session_state["pagina"] = "homepage"
                st.rerun()
            st.stop()
        cliente = st.selectbox(
            "Selecione o cliente",
            df_clientes["nome"].to_list(),
        )
        divida = select_debt_by_client(
            cliente,
        )
        st.subheader(f"**Divida do cliente** :gray[__{cliente}__]", divider="orange")
        st.markdown(
            f"""<p style="display: flex; justify-content: space-between; align-items: center; font-size: 30px; background-color: #8B4513; padding: 10px; border-radius: 8px;">
            <span>Valor atual:</span>
            <span style="text-decoration: underline; color: white; font-weight: bold;">R$ {divida if divida else 0.00}</span>
            </p>""",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns([4, 1])
        dividas_completa = select_all_sales_by_client(cliente)
        with col1.popover(
            "Consulta completa", help="Consulte todas as dividas do cliente"
        ):
            if dividas_completa is not None:
                df_dividas_total = dividas_completa
                logger.debug(df_dividas_total)
                df_dividas_total["preco"] = df_dividas_total["preco"].map(
                    lambda x: f"R$ {x:.2f}".replace(".", ",")
                )
                df_dividas_total["total"] = df_dividas_total["total"].map(
                    lambda x: f"R$ {x:.2f}".replace(".", ",")
                )
                df_dividas_total["data"] = df_dividas_total["data"].map(
                    lambda x: x.strftime("%d/%m/%Y, %H:%M:%S")
                )
                df_dividas_total.columns = [
                    "Nome",
                    "Produto",
                    "Preço",
                    "Quantidade",
                    "Valor Final",
                    "Data",
                ]
                st.table(df_dividas_total)
        try:
            col2.download_button(
                label="Baixar planilha .xlsx",
                help="Baixe todas as dividas do cliente",
                icon="🗃️",
                data=converter_df_to_excel(dividas_completa),
                file_name="divida.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
            )
        except Exception as e:
            st.warning(f"Não dividas existentes para o cliente {cliente}")
            st.button("Dowload divida", disabled=True)
            Logger.error(str(e))
        if st.sidebar.button("ir para home", use_container_width=True, type="primary"):
            st.session_state["pagina"] = "homepage"
            st.rerun()
    else:
        st.title("Consulta de Dívida de Clientes")

        with st.form(key="consulta_form"):
            cliente = st.text_input(
                "Email de cadastro",
                help="Digite o seu email completo como no cadastro",
                value=st.session_state["username"],
            )
            cpf = st.text_input(
                "CPF",
                help="Digite seu cpf completo como no cadastro, sem caracteres",
                max_chars=14,
                placeholder="123.456.789-00",
            )
            # print('cpf:',cpf)
            consultar = st.form_submit_button(
                "Consultar", icon="🔍", help="Consultar divida do cliente"
            )
        if not cpf or not cliente:
            st.info("Obs: Preencha todos os campos para consultar")
        else:
            if consultar:
                divida = select_debt_by_client(cliente, str_as_number(cpf))
                st.write(
                    f"Divida do cliente {cliente}: R$ {divida if divida else 0.00}"
                )
                divida_total = select_all_sales_by_client(cliente, str_as_number(cpf))

                if divida_total is not None:
                    df_dividas_total = DataFrame(divida_total)
                    df_dividas_total["preco"] = df_dividas_total["preco"].map(
                        lambda x: f"R$ {x:.2f}".replace(".", ",")
                    )
                    df_dividas_total["total"] = df_dividas_total["total"].map(
                        lambda x: f"R$ {x:.2f}".replace(".", ",")
                    )
                    df_dividas_total["data"] = df_dividas_total["data"].map(
                        lambda x: x.strftime("%d/%m/%Y, %H:%M:%S")
                    )
                    df_dividas_total.columns = [
                        "Nome",
                        "Produto",
                        "Preço",
                        "Quantidade",
                        "Valor Final",
                        "Data",
                    ]
                    st.table(df_dividas_total)
                    st.download_button(
                        label="Download divida",
                        data=converter_df_to_excel(divida_total),
                        file_name="divida.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.error("Nenhuma divida encontrado !!!")

        if st.sidebar.button("ir para home", use_container_width=True, type="primary"):
            st.session_state["pagina"] = "homepage"
            st.rerun()


def atualizar_divida():
    """Pagina para atualizar a dívida de clientes"""
    st.title("Atualizar Dívida de Clientes")
    df_clientes = select_all_clientes()
    df_produtos = select_all_products()
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
        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            step=1,
            max_value=ProductRepository().select_product(produto).estoque,
        )
        st.markdown(
            f"<span style='font-size:30px; text-decoration:underline;'>Valor final: :green[${preco * quantidade if (preco and quantidade) is not None else 0}]</span>",
            unsafe_allow_html=True,
        )
        if st.button("Atualizar", type="primary", disabled=df_produtos.empty):
            is_register = register_sale(cliente, produto, quantidade)
            if is_register:
                st.success(
                    f"Venda registrada com sucesso no valor de R${preco * quantidade}!"
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

    if st.sidebar.button("ir para home", use_container_width=True, type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
