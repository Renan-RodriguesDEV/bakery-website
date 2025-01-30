import streamlit as st

from src.models.repository.user_repository import UserRepository
from src.models.repository.dataframes_repository import select_all_clientes


def information():
    st.title("Informações de clientes")
    cliente = st.selectbox("Selecione o cliente", select_all_clientes())
    if st.button("Consultar") and cliente:
        cliente_obj = None
        with UserRepository() as c:
            cliente_obj = c.select_user(cliente)
        if cliente_obj:
            st.subheader(f"Informações sobre: {cliente}")
            st.markdown(
                f"""
                <div style="background-color: #393d4d; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #aaa; margin-bottom: 15px;">Detalhes do Cliente</h3>
                    <div style="margin-left: 10px;">
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Nome:</strong> {cliente_obj.nome}</p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Telefone:</strong> <a href="https://wa.me/+55{cliente_obj.telefone}" style="color: #00e676;">{cliente_obj.telefone}</a></p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Email:</strong> <a href="mailto:{cliente_obj.email}" style="color: #00e676;">{cliente_obj.email}</a></p>
                    </div>
                </div>
                <br></br>
                """,
                unsafe_allow_html=True,
            )
    if st.button("Voltar", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
