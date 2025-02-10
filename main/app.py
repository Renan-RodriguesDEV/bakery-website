import streamlit as st
from routes.minhas_compras_page import minhas_compras
from src.models.repository.user_repository import UserRepository
from routes.carrinho_compras_page import shopping_cart
from routes.user_page import information, my_account
from routes.cadastros_page import cadastro_cliente, cadastro_produto
from routes.compras_page import realizar_compra
from routes.login_page import tela_login
from routes.dividas_page import atualizar_divida, consulta_divida
from routes.product_page import consulta_produto
from routes.support_page import esquci_senha, page_support
from src.utils.uteis import Logger

st.set_page_config(
    page_title="Sistema de Gerenciamento de Vendas",
    page_icon=":moneybag:",
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


@throws_exception
# Função para a renderizar a homepage
def homepage():
    nome_de_sessao = (
        UserRepository()
        .select_user(st.session_state["username"], st.session_state["usuario"])
        .nome
    )
    st.session_state["nome_de_sessao"] = nome_de_sessao
    st.markdown(
        f"<h1 style='font-size:33px; color:darkgray;'>Bem vindo de volta, <span style='color:#8B4513';font-style:italic;>{st.session_state['nome_de_sessao']}<span/>!</h1>",
        unsafe_allow_html=True,
    )
    st.html(
        f"<h2 style='color:darkgray'>Status de login: <span style='color:#DAA520'> {st.session_state['usuario']}<span/></h2>"
    )
    x, y = st.columns([2, 1], gap="small", vertical_alignment="top")

    # Coordenadas da itai
    latitude, longitude = -23.406600592923784, -49.09880181525712
    x.markdown(
        "<span style='color:#8B4513'>Estamos localizados em</span> 📍:",
        unsafe_allow_html=True,
    )
    x.map(
        data={"latitude": [latitude], "longitude": [longitude]},
        use_container_width=True,
        color="#DAA520",
        height=250,
        size=(50, 50),
    )

    if not st.session_state["owner"]:
        top_nav = y.container()
        with top_nav:
            _, cart_col = st.columns([8, 1])
            with cart_col:
                if st.button("🛒", key="btn_cart_top", help="carrinho de compras"):
                    st.session_state["pagina"] = "cart"
                    st.rerun()
        if y.button("Comprar", use_container_width=True, help="faça suas compras"):
            st.session_state["pagina"] = "realizar_compra"
            st.rerun()
    if st.session_state["owner"]:
        if y.button(
            "Cadastro/Alteração de Produtos",
            use_container_width=True,
        ):
            st.session_state["pagina"] = "cadastro_produto"
            st.rerun()
    if st.session_state["owner"]:
        if y.button(
            "Cadastro/Alteração de Clientes",
            use_container_width=True,
        ):
            st.session_state["pagina"] = "cadastro_cliente"
            st.rerun()

    if y.button("Catalogo de Produtos", use_container_width=True):
        st.session_state["pagina"] = "consulta_produto"
        st.rerun()

    if y.button("Consultar Pendencias", use_container_width=True):
        st.session_state["pagina"] = "consulta_divida"
        st.rerun()

    if not st.session_state["owner"]:
        if y.button("Minhas compras", use_container_width=True):
            st.session_state["pagina"] = "minhas_compras"
            st.rerun()

    if st.session_state["owner"]:
        if y.button(
            "Alterar Pendencias",
            use_container_width=True,
        ):
            st.session_state["pagina"] = "atualizar_divida"
            st.rerun()

    if st.sidebar.button(
        "Sair",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["autenticado"] = False
        st.session_state["pagina"] = "login"
        st.rerun()

    if st.sidebar.button(
        "Suporte ao Usuario",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "suporte"
        st.rerun()
    if st.sidebar.button(
        "Minha Conta",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "conta"
        st.rerun()

    if st.session_state["owner"]:
        if st.sidebar.button(
            "Informações de Clientes",
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
if not "owner" in st.session_state or not st.session_state["owner"]:
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
    if st.session_state["pagina"] == "support":
        page_support()
    elif st.session_state["pagina"] == "esqueci":
        esquci_senha()
    else:
        tela_login()
