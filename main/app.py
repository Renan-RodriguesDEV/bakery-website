import time
import streamlit as st
from routes.carrinho_compras_page import shopping_cart
from routes.user_page import information
from src.utils.email import EmailSender
from routes.cadastros_page import cadastro_cliente, cadastro_produto, my_account
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
    initial_sidebar_state="collapsed",
)

Logger.info("[==] Runnig server streamlit localhost in http://localhost:8501/ [==]")


# Função para enviar feedback
@st.cache_data
def send_feedback(feedback):
    try:
        EmailSender().send_feedback_email(str(st.session_state["username"]), feedback)

        return True
    except Exception as e:
        Logger.error(str(e))
        return False


# Função para a homepage
def homepage():
    st.markdown(
        f"<h1 style='font-size:33px; color:white;'>Bem-vindo, <span style='color:red';font-style:italic;>{st.session_state['username']}<span/>!</h1>",
        unsafe_allow_html=True,
    )
    st.subheader(f"Você está logado como: :gray[{st.session_state['usuario']}]")
    x, y = st.columns([2, 1], gap="small", vertical_alignment="top")

    feedback = x.text_area(
        "Feedback do cliente",
        placeholder="Deixe seu feedback aqui",
        max_chars=255,
        height=200,  # Define a altura fixa para o text_area
        help="O feedback é importante para melhorar a experiência do usuário, todos os feedbacks serão enviados para o email do proprietário",
    )
    stars = x.feedback(options="stars")
    feedback += "\n" + f"Stars: {stars}"
    if x.button("Enviar Feedback", type="primary"):

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

    # Botão de Carrinho fixo na parte superior da página
    # Posicionado à direita do header
    top_nav = y.container()
    with top_nav:
        _, cart_col = st.columns([8, 1])
        with cart_col:
            if st.button("🛒", key="btn_cart_top", disabled=st.session_state["owner"]):
                st.session_state["pagina"] = "cart"
                st.rerun()
    if y.button(
        "Comprar",
        use_container_width=True,
        disabled=st.session_state["owner"],
    ):
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

    if st.session_state["owner"]:
        if y.button(
            "Alterar Pendencias",
            use_container_width=True,
        ):
            st.session_state["pagina"] = "atualizar_divida"
            st.rerun()

    if st.sidebar.button(
        "Logout",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["autenticado"] = False
        st.session_state["pagina"] = "login"
        st.rerun()

    if st.sidebar.button(
        "Support Page",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "suporte"
        st.rerun()
    if st.sidebar.button(
        "My Account",
        use_container_width=True,
    ):
        st.session_state["pagina"] = "conta"
        st.rerun()
    if st.sidebar.button(
        "Informações de Clientes",
        use_container_width=True,
        disabled=not st.session_state["owner"],
        type="primary",
    ):
        st.session_state["pagina"] = "informacoes"
        st.rerun()
    st.html(
        """
    <style>
    div[data-testid="stSidebarCollapsedControl"] button {
        background-color: red ;
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
    st.session_state["usuario"] = "Client"
else:
    st.session_state["usuario"] = "Owner/Employee"
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

else:
    # Se não estiver autenticado, ainda permite acesso à página de suporte
    if st.session_state["pagina"] == "support":
        page_support()
    elif st.session_state["pagina"] == "esqueci":
        esquci_senha()
    else:
        tela_login()
