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
from src.models.repository.user_repository import UserRepository
from src.utils.email import EmailSender
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
        st.title("Consulta de pendências de Clientes")
        st.subheader(
            ":grey[Consulte as pendências de dívidas dos clientes, para que possam ser atualizadas.]"
        )
        df_clientes = select_all_clientes()
        if df_clientes.empty:
            st.subheader("Ops!! Houve algum erro no processo..")
            st.error("Nenhum cliente cadastrado")
            st.warning("Cadastre algum cliente antes de acessar está pagina")
            if st.sidebar.button(
                "Home",
                icon=":material/home:",
                help="Ir para homepage",
                use_container_width=True,
                type="primary",
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
        st.subheader(f"**Cliente**: :gray[{cliente}]", divider="orange")
        divida_total = divida if divida else 0.00
        divida_display = (
            f"R$ {float(divida_total):.2f}".replace(".", ",")
            if divida_total is not None
            else "R$ 0,00"
        )

        st.html(
            f"""
            <!-- Bootstrap + Icons -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">

            <div class="container-fluid p-0 my-3">
              <div class="card bg-transparent border-0 text-light" style="background: rgba(20,20,20,0.28); backdrop-filter: blur(6px); border-radius:12px; border:1px solid rgba(255,255,255,0.04); padding:14px;">
                <div class="d-flex align-items-center justify-content-between w-100">
                  <div>
                    <small style="letter-spacing:0.6px; text-transform:uppercase; color:#bdbdbd; font-weight:600;">Valor atual</small>
                    <div style="font-size:30px; font-weight:800; color:#ffffff; margin-top:6px;">{divida_display}</div>
                    <div style="margin-top:6px; color:#9e9e9e; font-size:13px;">Resumo rápido • <span style="color:#8B4513; font-weight:600;">visão proprietários</span></div>
                  </div>

                  <div class="text-end">
                    <div style="font-size:12px; color:#bfbfbf; margin-bottom:6px;">Status</div>
                    <div style="display:inline-flex; align-items:center; gap:8px; padding:8px 14px; border-radius:10px; background: rgba(0,0,0,0.35); border:1px solid rgba(139,69,19,0.12);">
                      <i class="bi bi-wallet2" style="color:#8B4513; font-size:18px;"></i>
                      <span style="color:#8B4513; font-weight:700; font-size:15px;">Saldo</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            """
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
        if st.sidebar.button(
            "Home",
            icon=":material/home:",
            help="Ir para homepage",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "homepage"
            st.rerun()
        if st.sidebar.button(
            "Editar pendencias",
            icon=":material/edit:",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "atualizar_divida"
            st.rerun()
    else:
        st.title("Consulta de pendencias de Clientes")
        st.subheader(
            ":grey[Consulte as pendências de dívidas dos clientes, para que possam ser atualizadas.]"
        )

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

        if st.sidebar.button(
            "Home",
            icon=":material/home:",
            help="Ir para homepage",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "homepage"
            st.rerun()


def atualizar_divida():
    """Pagina para atualizar a dívida de clientes"""
    st.title(
        """
Edite as pendências de dívidas dos clientes. 
    """
    )
    st.subheader(
        ":grey[Aqui você pode adicionar ou remover dívidas de clientes específicos.]"
    )
    df_clientes = select_all_clientes()
    df_produtos = select_all_products(200)
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
        preco = 0.0
        estoque = 0.0
        try:
            if produto:
                preco = ProductRepository().select_product_price(produto)
                estoque = ProductRepository().select_product(produto).estoque
        except Exception as e:
            st.warning("Produto não encontrado")
            Logger.error(str(e))
        quantidade = st.number_input(
            "Quantidade",
            min_value=0,
            step=1,
            max_value=estoque - 1 if estoque else 0,
            value=0,
            help=f"Estoque atual: {estoque}, coloque valores inteiros!",
        )
        valor_total = float(preco) * float(quantidade) if preco is not None else 0
        # Garantindo que os valores estão formatados corretamente antes de inserir no HTML
        preco_formatado = (
            f"R$ {preco:.2f}".replace(".", ",") if preco is not None else "R$ 0,00"
        )
        valor_total_formatado = (
            f"R$ {valor_total:.2f}".replace(".", ",")
            if valor_total is not None
            else "R$ 0,00"
        )

        # HTML simplificado para garantir compatibilidade
        st.html(
            f"""
            <div style="display:flex; flex-direction:column; gap:10px; padding:18px; border-radius:12px; background:#1e1e1e; border:1px solid #333; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                <div style="font-size:16px; color:#8B4513; font-weight:700; margin-bottom:8px; border-bottom:1px solid #444; padding-bottom:8px;">
                    Resumo da transação
                </div>
                
                <div style="display:flex; align-items:center; justify-content:space-between; gap:20px;">
                    <div style="flex:1; background:#2a2a2a; border-radius:8px; padding:12px; border-left:4px solid #8B4513;">
                        <div style="font-size:13px; color:#999; font-weight:600; margin-bottom:6px;">
                            <i class="fas fa-tag" style="margin-right:5px;"></i>Preço unitário
                        </div>
                        <div style="font-size:18px; font-weight:700; color:#eee;">{preco_formatado}</div>
                    </div>
                    
                    <div style="flex:1; background:#2a2a2a; border-radius:8px; padding:12px; border-left:4px solid #8B4513;">
                        <div style="font-size:13px; color:#999; font-weight:600; margin-bottom:6px;">
                            <i class="fas fa-cubes" style="margin-right:5px;"></i>Quantidade
                        </div>
                        <div style="font-size:18px; font-weight:700; color:#eee;">{quantidade}</div>
                    </div>
                </div>
                
                <div style="margin-top:10px; text-align:center;">
                    <div style="font-size:13px; color:#999; font-weight:600; margin-bottom:8px;">
                        <i class="fas fa-calculator" style="margin-right:5px;"></i>Valor final
                    </div>
                    <div style="display:inline-block; background:#212e21; color:#4ade80; padding:10px 16px; border-radius:10px; font-size:22px; font-weight:800; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
                        {valor_total_formatado}
                    </div>
                </div>
            </div>
            
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            """,
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
            valor_remover = divida_total
        if is_pag is not None and is_pag:
            st.success(
                f"Pagamento registrado com sucesso!! a conta atual está em R$ {select_debt_by_client(cliente)}"
            )
            # TODO: Enviar email de confirmação de pagamento
            send_notify(cliente, valor_remover)
        elif is_pag is None or not is_pag:
            st.warning("Aguardando efetuação de pagamento")
        else:
            st.error("Erro ao registrar a pagamento")

    if st.sidebar.button(
        "Home",
        icon=":material/home:",
        help="Ir para homepage",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["pagina"] = "homepage"
        st.rerun()
    if st.sidebar.button(
        "Consultar dividas",
        icon=":material/search:",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["pagina"] = "consulta_divida"
        st.rerun()
    if st.sidebar.button(
        "Editar produtos",
        icon=":material/edit:",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["pagina"] = "cadastro_produto"
        st.rerun()


@st.cache_data
def send_notify(cliente, valor):
    email_sender = EmailSender()
    cliente_email = UserRepository().select_user(cliente, "Cliente").email
    email_sender.send_email(
        email=cliente_email,
        text=f"Pagamento no valor de R${valor} registrado com sucesso!",
    )
    email_sender.send_email(
        email=st.secrets["USER"],
        text=f"Pagamento no valor de R${valor} registrado com sucesso!",
    )
    st.success(f"Cliente {cliente_email} e proprietário(s) notificados com sucesso!")
    st.balloons()
