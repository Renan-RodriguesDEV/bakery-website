import streamlit as st
from src.models.repository.user_repository import UserRepository
from src.utils.hasher import Hasher
from src.utils.uteis import Logger


def autenticar_usuario(username, password, type_user):
    """Verifica a senha e usuario no database

    Args:
        username (str): _username_
        password (str/sha56): _senha_
        type_user (str): tipo de login

    Returns:
        bool: usuario autenticado or not autenticado
    """
    if type_user == "Proprietario/Funcionario":
        Logger.info("Verificando Proprietario/Funcionario")
        user = UserRepository().select_user_by_email(username, type_user)
        if user:
            isAuth = Hasher().checkpswd(password, user.senha)
            if (username == user.email or user.nome == username) and isAuth:
                Logger.sucess("Logando o usuario")
                return True
            Logger.error(
                f"Erro ao logar o usuario {username}-{user.email} {password}-{user.senha}"
            )
        return False
    elif type_user == "Cliente":
        Logger.info("Verificando cliente")
        user = UserRepository().select_user_by_email(username, type_user)
        if not user:
            Logger.error(f"Usuario {username} não encontrado")
            return False
        Logger.error(f"[===] - User: {user.nome} [===] Password: {user.senha} - [===]")
        isAuth = Hasher().checkpswd(password, user.senha)
        if (username == user.nome or username == user.email) and isAuth:
            Logger.info("Autenticado com sucesso")
            return True
        Logger.error(f"Erro ao logar o usuario, {isAuth} | {username} | {user.nome}")
    return False


def tela_login():
    """Tela de login"""
    st.title(
        "Faça seu Login para continuar :grey[(_Escolha entre Proprietario/Funcionario_)]",
    )
    with st.form(key="form_login"):
        tipo_user = st.selectbox(
            ":gray[**Tipo de Usuário**]",
            ["Cliente", "Proprietario/Funcionario"],
            help="Login como usuario cliente e proprietario/funcionario",
        )
        Logger.sucess(tipo_user)
        username = st.text_input(":gray[Usuário]", help="Insira seu nome de usuario")
        password = st.text_input(
            ":gray[**Senha**]",
            type="password",
            max_chars=11,
            help="insira sua senha de usuario, clientes insiram o CPF cadastrado sem os caracteres",
        )

        if username == "" or password == "":
            st.warning("Por favor, preencha os campos de usuário e senha")
        x, y = st.columns([2, 1], gap="large")
        col1, col2 = x.columns([1, 1])
        if col1.form_submit_button("Login", type="primary"):
            try:
                has_auth = autenticar_usuario(username, password, type_user=tipo_user)
                if has_auth:
                    st.session_state["autenticado"] = True
                    st.session_state["usuario"] = tipo_user
                    st.session_state["username"] = username
                    if tipo_user == "Proprietario/Funcionario":
                        st.session_state["owner"] = True
                    else:
                        st.session_state["owner"] = False
                    Logger.info(
                        f"Usuario {username} logado com sucesso como: {tipo_user}"
                    )
                    st.session_state["pagina"] = "homepage"
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
            except Exception as e:
                Logger.error(str(e))
                st.error("Erro ao logar o usuário")
        if col2.form_submit_button(
            "Esqueci minha senha",
            help="Reseta senha enviando token por email!!",
            type="primary",
        ):
            st.session_state["pagina"] = "esqueci"
            st.rerun()
        if y.form_submit_button("Ajuda", help="Suporte ao usuario", type="secondary"):
            st.session_state["pagina"] = "suporte"
            st.rerun()
