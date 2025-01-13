import datetime
import streamlit as st

from src.utils.email import EmailSender
from src.models.repository.user_repository import UserRepository
from src.utils.uteis import generate_token


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
    if st.button("Voltar", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


def esquci_senha():
    """Pagina dedicada ao suporte ao usuario"""
    x, y = st.columns([2, 1], gap="large", vertical_alignment="bottom")
    x.title("Bem vindo a pagina de Reset de Senhas")
    usuario = x.text_input(
        "Por favor insira seu email de usuario ou nome caso seja Owner!!",
        type="default",
        max_chars=60,
    )
    type_user = y.selectbox("Qual seu tipo de Usuario?", ["Owner/Employee", "Client"])
    visible = False if type_user == "Owner/Employee" else True
    nova_senha = x.text_input(
        "Nova senha",
        type="password",
        max_chars=8,
        disabled=visible,
        help="Senhas de clientes serão token enviados via email para posteriormente realizar uma alteração em MyAccount",
    )
    if x.button("Recuperar Senha", type="primary"):
        with UserRepository() as user:
            new_pass = None
            token_generator = generate_token()
            if type_user == "Client":
                print(token_generator)
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
            else:

                new_pass = user.reset_password(usuario, nova_senha, type_user)
                if new_pass:
                    st.success(f"Nova senha gerada com sucesso!!")
                else:
                    st.error(f"Erro ao gerar nova senha!!")

    if not usuario or (not nova_senha and type_user == "Owner/Employee"):
        st.warning("Por favor preencha os campos de email e senha")
    y.write("Criador e support da pagina: @__little_renan.py")
    y.html(
        """<p>Caso tenha algum problema ou sugestão, por favor, entre em contato com o criador da pagina</p> <p>✉️ <a href='mailto:renanrodrigues7110.com target='_blank'>renanrodrigues7110@gmail.com</a>"""
    )
    # Adicione botão de voltar
    if st.button("Voltar", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
