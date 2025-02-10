import streamlit as st

from src.utils.email import EmailSender
from src.models.repository.dataframes_repository import select_all_sales_by_client


def notify_status(_to, message):
    """Função para solicitar status de pagamento"""

    EmailSender().send_email(
        _to, message, f"Solicitação de status de pagamento de {_to}"
    )


def minhas_compras():
    """Pagina de minhas compras"""
    st.title("Minhas Compras")

    st.html(
        "<h2 style='font-size:24px'>Altere status de entrege e veja suas compras ainda não retiradas!!</h2>"
    )
    comprinhas = select_all_sales_by_client(client_email=st.session_state["username"])
    st.write("---")
    if comprinhas is not None:
        x, y = st.columns([1, 1], vertical_alignment="center", gap="large")
        for i, compra in enumerate(comprinhas.values):
            with x.popover(
                compra[1],
                use_container_width=True,
                help="Clique para ver detalhes da compra",
                icon="📦",
            ):
                st.markdown(
                    f"""
                    <table style="
                        background-color: #8B4513;
                        border-radius: 10px;
                        padding: 15px;
                        margin: 10px 0;
                        text-align: center;
                        width: 100%;
                        border-collapse: collapse;
                    ">
                        <thead>
                            <tr>
                                <th style="color: white; padding: 10px;">Nome</th>
                                <th style="color: white; padding: 10px;">Quantidade</th>
                                <th style="color: white; padding: 10px;">Valor</th>
                                <th style="color: white; padding: 10px;">Valor Final</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="color: white; padding: 10px;">{compra[1]}</td>
                                <td style="color: white; padding: 10px;">{compra[3]}</td>
                                <td style="color: white; padding: 10px;">R$ {str(compra[2]).replace('.', ',')}</td>
                                <td style="color: #DAA520; padding: 10px;">R$ {str(compra[4]).replace('.', ',')}</td>
                            </tr>
                        </tbody>
                    </table>
                    """,
                    unsafe_allow_html=True,
                )

            col2, col3 = y.columns(2)
            if col2.button(
                "Já retirei",
                key=f"retirado_{i}",
                type="primary",
                use_container_width=True,
            ):
                st.success('Status atualizado para "Retirado"', icon="🫡")
                message = f"""<p>O cliente <b>{st.session_state['username']}</b> alterou o status da compra para <b>"já retirou"</b>, compra: <b>{compra[1]}</b>.</p>
                <table border="1" style="border-collapse: collapse; width:100%;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th>Nome</th>
                            <th>Quantidade</th>
                            <th>Valor</th>
                            <th>Valor Final</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{compra[1]}</td>
                            <td>{compra[3]}</td>
                            <td>R$ {str(compra[2]).replace('.',',')}</td>
                            <td>R$ {str(compra[4]).replace('.',',')}</td>
                        </tr>
                    </tbody>
                </table>
                <p>Verifique se já foi realizado o pagamento</p>
                """
                notify_status(st.session_state["username"], message)

                st.info("O vendedor foi notificado", icon="🔔")
                st.success(
                    "Aguarde até que o vendedor atualize o status de pagamento",
                    icon="🍵",
                )
            if col3.button(
                "Vou retirar",
                key=f"vou_retirar_{i}",
                type="secondary",
                use_container_width=True,
            ):
                st.warning("Compareça até o local para retirar a compra")
                message = f"""<p>O cliente <b>{st.session_state['username']}</b> informou que irá retirar a compra.</p>
                <table border="1" style="border-collapse: collapse; width:100%;">
                    <tr style="background-color: #f2f2f2;">
                        <th>Nome</th>
                        <th>Quantidade</th>
                        <th>Valor</th>
                        <th>Valor Final</th>
                    </tr>
                    <tr>
                        <td>{compra[1]}</td>
                        <td>{compra[3]}</td>
                        <td>R$ {str(compra[2]).replace('.',',')}</td>
                        <td>R$ {str(compra[4]).replace('.',',')}</td>
                    </tr>
                </table>
                """
                notify_status(st.session_state["username"], message)
                st.info("O vendedor foi notificado", icon="🔔")

    else:
        st.info("Não há compra(s) para retirarda(s) ou atualização de status !!!")
    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
