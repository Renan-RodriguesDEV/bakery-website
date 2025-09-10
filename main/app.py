import streamlit as st
from routes.cadastros_page import (
    cadastro_cliente,
    cadastro_produto,
    customer_registration,
)
from routes.carrinho_compras_page import shopping_cart
from routes.compras_page import realizar_compra
from routes.dividas_page import atualizar_divida, consulta_divida
from routes.login_page import tela_login
from routes.minhas_compras_page import minhas_compras
from routes.notifications import modal_notifications
from routes.product_page import consulta_produto
from routes.support_page import esquci_senha, page_support
from routes.user_page import information, my_account
from src.models.repository.notifications_repository import notifications_repository
from src.models.repository.user_repository import UserRepository
from src.style.style import get_config_map, load_css
from src.utils.uteis import Logger

st.set_page_config(
    page_title="Sistema de Gerenciamento de Vendas",
    page_icon=":bakery:",
    layout="wide",
    initial_sidebar_state="expanded",
)


Logger.info("[==] Runnig server streamlit localhost in http://localhost:8501/ [==]")


def throws_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            Logger.error(f"Erro: {e}")
            st.error("Ocorreu um erro inesperado")
            for key in st.session_state.keys():
                del st.session_state[key]
            return tela_login()

    return wrapper


load_css("header.css")
load_css("sidebar.css")
load_css("listtemplate.css")
load_css("background.css")


@throws_exception
# Função para a renderizar a homepage
def homepage():
    load_css("homepage.css")
    if st.session_state.get("owner"):
        load_css("notify.css")
        # botão com contador
        count_unread = notifications_repository.get_count_unread_notifications()
        if st.button(
            f"+{count_unread}",
            icon=":material/notifications:",
            type="primary",
            help="Notificações não lidas",
            key="notifications",
        ):
            # abre popover listando notificações
            modal_notifications(notifications_repository)
    nome_de_sessao = (
        UserRepository()
        .select_user(st.session_state["username"], st.session_state["usuario"])
        .nome
    )
    st.session_state["nome_de_sessao"] = nome_de_sessao
    name_header = (
        str(nome_de_sessao).split(" ")[0] + " " + str(nome_de_sessao).split(" ")[-1]
    )
    st.markdown(
        f"""
        <div style='text-align: center; padding: 8px;'>
            <h1 style='font-size: 32px; color: black;'>
                Olá, <span style='color: #8B4513; font-weight: bold;'>{name_header}</span>!
            </h1>
            <p style='font-size: 24px; color: #313; font-style: italic;'>
                Seja bem-vindo(a) ao nosso sistema de vendas
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    x, y = st.columns([2, 2], gap="large", vertical_alignment="top")

    # Coordenadas da itai
    latitude, longitude = -23.406600592923784, -49.09880181525712
    y.markdown(
        get_config_map(latitude=latitude, longitude=longitude),
        unsafe_allow_html=True,
    )
    y.map(
        data={"latitude": [latitude], "longitude": [longitude]},
        use_container_width=True,
        color="#DAA520",
        height=250,
        size=(50, 50),
    )

    if not st.session_state["owner"]:
        top_nav = x.container()
        with top_nav:
            cart_col, _ = st.columns([8, 1])
            with cart_col:
                if st.button(
                    "",
                    key="btn_cart_top",
                    help="carrinho de compras",
                    type="primary",
                    icon=":material/shopping_cart:",
                ):
                    st.session_state["pagina"] = "cart"
                    st.rerun()
        if x.button(
            "Comprar",
            use_container_width=True,
            help="faça suas compras",
            type="primary",
            icon=":material/add_shopping_cart:",
        ):
            st.session_state["pagina"] = "realizar_compra"
            st.rerun()
    if st.session_state["owner"]:
        if x.button(
            "Editar de Produtos",
            icon=":material/edit:",
            use_container_width=True,
            type="primary",
            help="cadastre ou altere produtos",
        ):
            st.session_state["pagina"] = "cadastro_produto"
            st.rerun()
    if st.session_state["owner"]:
        if x.button(
            "Editar de Clientes",
            icon=":material/edit:",
            use_container_width=True,
            type="primary",
            help="cadastre ou altere clientes",
        ):
            st.session_state["pagina"] = "cadastro_cliente"
            st.rerun()

    if x.button(
        "Catalogo de Produtos",
        icon=":material/store:",
        use_container_width=True,
        type="primary",
        help="consulte produtos",
    ):
        st.session_state["pagina"] = "consulta_produto"
        st.rerun()

    if x.button(
        "Consultar Pendencias",
        icon=":material/search:",
        use_container_width=True,
        type="primary",
        help="consulte pendencias",
    ):
        st.session_state["pagina"] = "consulta_divida"
        st.rerun()

    if not st.session_state["owner"]:
        if x.button(
            "Minhas compras",
            use_container_width=True,
            type="primary",
            help="consulte suas compras",
            icon=":material/cases:",
        ):
            st.session_state["pagina"] = "minhas_compras"
            st.rerun()

    if st.session_state["owner"]:
        if x.button(
            "Editar Pendencias",
            icon=":material/edit:",
            use_container_width=True,
            type="primary",
            help="altere pendencias",
        ):
            st.session_state["pagina"] = "atualizar_divida"
            st.rerun()

    if st.sidebar.button(
        "Sair",
        icon=":material/logout:",
        help="Sair do sistema",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["autenticado"] = False
        st.session_state["pagina"] = "login"
        st.rerun()

    if st.sidebar.button(
        "Suporte ao Usuario",
        icon=":material/help:",
        help="Suporte ao usuario",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "suporte"
        st.rerun()
    if st.sidebar.button(
        "Minha Conta",
        icon=":material/account_circle:",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "conta"
        st.rerun()

    if st.session_state["owner"]:
        if st.sidebar.button(
            "Informações de Clientes",
            icon=":material/info:",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "informacoes"
            st.rerun()

    st.html(
        """
    <style>
    div[data-testid="stSidebarCollapsedControl"] button {
        background-color: #DAA520 ;
        color: white ;
    }
    </style>
    """,
    )


# Configurando a sessão para manter o estado do login e da página
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"  # Define a página inicial como login
# Inicializa "owner" com False por padrão, caso ainda não tenha sido definido
if "owner" not in st.session_state or not st.session_state["owner"]:
    st.session_state["owner"] = False
    st.session_state["usuario"] = "Cliente"
else:
    st.session_state["usuario"] = "Proprietario/Funcionario"
# Verifica se o usuário está autenticado
if st.session_state["autenticado"]:
    if st.session_state["pagina"] == "homepage":
        homepage()
    elif st.session_state["pagina"] == "cadastro_produto":
        cadastro_produto()
    elif st.session_state["pagina"] == "cadastro_cliente":
        cadastro_cliente()
    elif st.session_state["pagina"] == "consulta_produto":
        consulta_produto()
    elif st.session_state["pagina"] == "consulta_divida":
        consulta_divida()
    elif st.session_state["pagina"] == "atualizar_divida":
        atualizar_divida()
    elif st.session_state["pagina"] == "realizar_compra":
        realizar_compra()
    elif st.session_state["pagina"] == "suporte":
        page_support()
    elif st.session_state["pagina"] == "conta":
        my_account()
    elif st.session_state["pagina"] == "esqueci":
        esquci_senha()
    elif st.session_state["pagina"] == "cart":
        shopping_cart()
    elif st.session_state["pagina"] == "informacoes":
        information()
    elif st.session_state["pagina"] == "minhas_compras":
        minhas_compras()

else:
    # Se não estiver autenticado, ainda permite acesso à página de suporte
    if st.session_state["pagina"] == "suporte":
        page_support()
    elif st.session_state["pagina"] == "esqueci":
        esquci_senha()
    elif st.session_state["pagina"] == "customer_registration":
        customer_registration()
    else:
        tela_login()
