from src.utils.uteis import Logger
import streamlit as st

from src.models.repository.database_repository import (
    select_user,
    select_user_client,
)


# Função de autenticação simulada (exemplo simples)
@st.cache_data
def autenticar_usuario(username, password, type_user):
    if type_user == "Owner/Employee":
        user = select_user(username, password)
        Logger.log_red(
            f'[===] - User: {user.get("username")} [===] Password: {user.get("password")} - [===]'
        )
        # Aqui você pode adicionar lógica de verificação com um banco de dados ou API
        if username == user.get("username") and password == user.get("password"):
            Logger.log_blue("Logando o usuario")
            return True
        Logger.log_red(
            f"Erro ao logar o usuario {username}-{user.get('username')} {password}-{user.get('password')}"
        )
        return False
    elif type_user == "Client":
        user = select_user_client(username, password)
        Logger.log_red(
            f'[===] - User: {user.get("username")} [===] Password: {user.get("password")} - [===]'
        )
        # Aqui você pode adicionar lógica de verificação com um banco de dados ou API
        if username == user.get("username") and password == user.get("password"):
            return True
        return False
    return False


# Modificação na função tela_login
def tela_login():
    st.title("Faça seu Login para continuar")
    tipo_user = st.selectbox("Usuario", ["Owner/Employee", "Client"])
    Logger.log_blue(tipo_user)
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
        if autenticar_usuario(username, password, type_user=tipo_user):
            st.session_state["autenticado"] = True
            st.session_state["owner"] = True if tipo_user == "Owner/Employee" else False
            st.session_state["usuario"] = username
            st.session_state["pagina"] = "homepage"  # Redireciona para a homepage
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    if col2.button(
        "Esqueci minha senha",
        help="Reseta senha enviando token por email!!",
        type="primary",
    ):
        st.session_state["pagina"] = "reset_password"
        st.rerun()
    if y.button("Support Page"):
        st.session_state["pagina"] = "support"
        st.rerun()
