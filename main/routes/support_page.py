import streamlit as st

from src.utils.uteis import send_feedback_email


def page_support():
    """Pagina dedicada ao suporte ao usuario"""
    x, y = st.columns([2, 1], gap="large", vertical_alignment="center")
    x.title("Bem vindo a pagina de support")
    feedback = x.text_area("Por favor descreva o ocorrido!!:", max_chars=500)
    if x.button("Enviar Feedback", type="primary"):
        send_feedback_email(name=st.session_state["usuario"], feedback=feedback)

    y.write("Criador e support da pagina: @__little_renan.py")
    y.html(
        """<p>Caso tenha algum problema ou sugestão, por favor, entre em contato com o criador da pagina</p> <p>✉️ <a href='mailto:renanrodrigues7110@gmail.com' target='_blank'>renanrodrigues7110@gmail.com</a></p><p>📞 <a href='https://wa.me/+5519998722472' target='_blank'>(19) 99872-2472</a></p>"""
    )
    # Adicione botão de voltar
    if st.button("Voltar", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
