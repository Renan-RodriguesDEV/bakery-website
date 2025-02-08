import datetime
import time
import streamlit as st

from src.utils.email import EmailSender
from src.models.repository.user_repository import UserRepository
from src.utils.uteis import Logger, generate_token


def page_support():
    """Pagina dedicada ao suporte ao usuario"""
    x, y = st.columns([2, 1], gap="large", vertical_alignment="center")
    x.title("Bem vindo a pagina de support")
    feedback = x.text_area("Por favor descreva o ocorrido!!", max_chars=500, height=200)

    if x.button("Enviar Feedback", type="primary"):
        EmailSender().send_feedback_email(
            name=st.session_state["usuario"], feedback=feedback
        )

    y.write("Criador e support da pagina: @__little_renan.py")
    y.html(
        """<p>Caso tenha algum problema ou sugestão, por favor, entre em contato com o criador da pagina</p> <p>✉️ <a href='mailto:renanrodrigues7110@gmail.com' target='_blank'>renanrodrigues7110@gmail.com</a></p><p>📞 <a href='https://wa.me/+5519998722472' target='_blank'>(19) 99872-2472</a></p>"""
    )
    # Adicione botão de voltar
    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


def esquci_senha():
    """Pagina dedicada ao suporte ao usuario"""
    x, y = st.columns([2, 1], gap="large", vertical_alignment="bottom")
    x.title("Bem vindo a pagina de Reset de Senhas")
    usuario = x.text_input(
        "Por favor insira seu email de usuario ou email de desenv. caso seja Funcionario!!",
        type="default",
        max_chars=60,
    )
    type_user = y.selectbox(
        "Qual seu tipo de Usuario?", ["Proprietario/Funcionario", "Cliente"]
    )

    if x.button("Recuperar Senha", type="primary"):
        with UserRepository() as user:
            new_pass = None
            token_generator = generate_token()
            user.set_token(token_generator)
            new_pass = user.reset_password(usuario, token_generator, type_user)
            if new_pass:
                st.success(
                    f"Nova senha gerada com sucesso!! {datetime.datetime.now().date()}"
                )
                st.text("seu novo token:")
                st.code(token_generator)
                EmailSender().send_email(
                    usuario,
                    f"""
<p>Seu <b>token</b> de usuário para login em <a href='https://bakery-of-village.streamlit.app/' style='color:blue;'>Padaria da Vila</a> é: <code>{token_generator}</code></p>
<p>Em seu próximo <i>login</i>, utilize-o para acessar sua conta em nosso site!</p>
<p>Atenciosamente,</p>
<p style='color:blue;'>Padaria da Vila - Itai/SP</p>
<p>Fone: <span style='color:green;'>(19) 99872-2472/SP</span></p>
<p><a href='https://bakery-of-village.streamlit.app/' style='color:blue; text-decoration:none;'>https://bakery-of-village.streamlit.app/</a></p>
                    """,
                )
            else:
                st.error(f"Erro ao gerar nova senha!!")

    y.write("Criador e support da pagina: @__little_renan.py")
    y.html(
        """<p>Caso tenha algum problema ou sugestão, por favor, entre em contato com o criador da pagina</p> <p>✉️ <a href='mailto:renanrodrigues7110.com target='_blank'>renanrodrigues7110@gmail.com</a>"""
    )
    # Adicione botão de voltar
    if st.sidebar.button("Voltar", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para enviar feedback
@st.cache_data
def send_feedback(feedback):
    try:
        EmailSender().send_feedback_email(str(st.session_state["username"]), feedback)

        return True
    except Exception as e:
        Logger.error(str(e))
        return False


def feedback_client():

    feedback = st.text_area(
        "Feedback do cliente",
        placeholder="Deixe seu feedback aqui",
        max_chars=255,
        height=200,  # Define a altura fixa para o text_area
        help="O feedback é importante para melhorar a experiência do usuário, todos os feedbacks serão enviados para o email do proprietário",
    )
    stars = st.feedback(options="stars")
    feedback += "\n" + f"Stars: {stars}"
    if st.button("Enviar Feedback", type="primary"):

        with st.status(
            "Enviando feedback...", expanded=True, state="running"
        ) as status:
            boolean = send_feedback(feedback)
            if boolean:
                status.update(state="complete")
                st.success(
                    f"Feedback enviado com sucesso: {st.session_state['username']}"
                )
        time.sleep(3)
        st.rerun()
