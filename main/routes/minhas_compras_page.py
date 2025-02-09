import streamlit as st

from src.utils.email import EmailSender
from src.models.repository.dataframes_repository import select_all_sales_by_client


def notify_payment_update(_to, value, buy):
    """Função para solicitar status de pagamento"""
    msg_html = f"""<h2>Solicitação de atualização no status de pagamento</h2>
    <p><b>{_to}</b>, soliçita uma atualização no pagamento de <b>{buy}</b> no valor de <b>{value}</b>, para pago!!<p/>
    <p>Por favor verifique o status do pagamento na plataforma e atualize no sistema</p>
    """
    EmailSender().send_email(
        _to, msg_html, f"Solicitação de status de pagamento de {_to}"
    )


def minhas_compras():
    """Pagina de minhas compras"""
    st.title("Minhas Compras")

    st.html(
        "<h2 style='font-size:24px'>Altere status de entrege e veja suas compras ainda não retiradas!!</h2>"
    )

    comprinhas = select_all_sales_by_client(st.session_state["username"])
    st.write("---")
    if comprinhas is not None:
        x, y = st.columns([1, 1], vertical_alignment="center", gap="large")
        for i, compra in enumerate(comprinhas.values):
            x.markdown(
                f"""
                <div style='
                    background-color: #8B4513;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    text-align: center;
                '>
                    <p style='
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        margin: 0;
                    '>{compra[1]}<br>
                    R$ {str(compra[2]).replace('.',',')} x {compra[3]} = <span style='color:#DAA520'>R$ {str(compra[4]).replace('.',',')}</span></p>
                </div>
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
                notify_payment_update(
                    st.session_state["username"],
                    f"R$ {str(compra[4]).replace('.',',')}",
                    compra[1],
                )
                st.success('Status atualizado para "Retirado"', icon="🫡")
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

    else:
        st.info("Não há compra(s) para retirarda(s) ou atualização de status !!!")
    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
