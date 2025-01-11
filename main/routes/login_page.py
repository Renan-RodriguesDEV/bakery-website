import streamlit as st
from src.models.repository.user_repository import UserRepository
from src.utils.hasher import Hasher
from src.utils.uteis import Logger


def autenticar_usuario(username, password, type_user):
    if type_user == "Owner/Employee":
        Logger.info(password)
        user = UserRepository().select_user(username, type_user)
        Logger.sucess(user)
        if user:
            isAuth = Hasher().checkpswd(password, user.senha)
            if (username == user.email or user.nome == username) and isAuth:
                Logger.sucess("Logando o usuario")
                return True
            Logger.error(
                f"Erro ao logar o usuario {username}-{user.email} {password}-{user.senha}"
            )
        return False
    elif type_user == "Client":
        user = UserRepository().select_user(username, type_user)
        if not user:
            Logger.error(f"Usuario {username} não encontrado")
            return False
        Logger.error(f"[===] - User: {user.nome} [===] Password: {user.cpf} - [===]")
        isAuth = Hasher().checkpswd(password, user.cpf)
        if (username == user.nome or username == user.email) and isAuth:
            Logger.info("Autenticado com sucesso")
            return True
        Logger.error(f"Erro ao logar o usuario, {isAuth} | {username} | {user.nome}")
    return False


# Modificação na função tela_login
def tela_login():
    st.title("Faça seu Login para continuar")
    tipo_user = st.selectbox("Usuario", ["Owner/Employee", "Client"])
    Logger.sucess(tipo_user)
    username = st.text_input("Usuário", help="Insira seu nome de usuario")
    password = st.text_input(
        "Senha",
        type="password",
        max_chars=11,
        help="insira sua senha de usuario, clientes insiram o CPF cadastrado",
    )

    if username == "" or password == "":
        st.warning("Por favor, preencha os campos de usuário e senha")
    x, y = st.columns([2, 1], gap="large")
    col1, col2 = x.columns([1, 1])
    if col1.button("Login", type="primary"):
        try:
            has_auth = autenticar_usuario(username, password, type_user=tipo_user)
            if has_auth:
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = tipo_user
                st.session_state["username"] = username
                if tipo_user == "Owner/Employee":
                    st.session_state["owner"] = True
                else:
                    st.session_state["owner"] = False
                Logger.info(f"Usuario {username} logado com sucesso como: {tipo_user}")
                st.session_state["pagina"] = "homepage"  # Redireciona para a homepage
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
        except Exception as e:
            Logger.error(str(e))
            st.error("Erro ao logar o usuário")
    if col2.button(
        "Esqueci minha senha",
        help="Reseta senha enviando token por email!!",
        type="primary",
    ):
        st.session_state["pagina"] = "esqueci"
        st.rerun()
    if y.button("Support Page"):
        st.session_state["pagina"] = "suporte"
        st.rerun()
