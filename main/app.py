import streamlit as st
from src.utils.email import EmailSender
from routes.cadastro import cadastro_cliente, cadastro_produto, my_account
from routes.compras import realizar_compra
from routes.login_page import tela_login
from routes.product_page import atualizar_divida, consulta_divida, consulta_produto
from routes.support_page import esquci_senha, page_support
from src.models.entities.database import initialize_database
from src.utils.uteis import Logger

Logger.log_green(
    "[==] Runnig server streamlit localhost in http://localhost:8501/ [==]"
)


initialize_database()


def load_styles():
    """Carrega o arquivo css para estilizaçção de componentes"""
    with open("style/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Sistema de Gerenciamento de Vendas",
    page_icon=":moneybag:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# load_styles()


# Função para enviar feedback
@st.cache_data
def send_feedback(feedback):
    EmailSender().send_feedback_email(str(st.session_state["username"]), feedback)
    st.success(f"Feedback enviado com sucesso: {st.session_state['username']}")


# Função para a homepage
def homepage():
    st.title(f"Bem-vindo, :gray[{st.session_state['username']}!]")
    st.subheader(f"Você está logado como: :gray[{st.session_state['usuario']}]")
    x, y = st.columns([2, 1], gap="medium", vertical_alignment="top")

    feedback = x.text_area(
        "Feedback do cliente",
        placeholder="Deixe seu feedback aqui",
        max_chars=255,
        height=280,  # Define a altura fixa para o text_area
        help="O feedback é importante para melhorar a experiência do usuário, todos os feedbacks serão enviados para o email do proprietário",
    )
    if x.button("Enviar Feedback", type="primary"):
        send_feedback(feedback)
    # Opções de navegação
    if y.button(
        "Buy",
        use_container_width=True,
        disabled=st.session_state["owner"],
    ):
        st.session_state["pagina"] = "realizar_compra"
        st.rerun()
    if y.button(
        "Cadastro de Produtos",
        use_container_width=True,
        disabled=not st.session_state["owner"],
    ):
        st.session_state["pagina"] = "cadastro_produto"
        st.rerun()
    if y.button(
        "Cadastro de Clientes",
        use_container_width=True,
        disabled=not st.session_state["owner"],
    ):
        st.session_state["pagina"] = "cadastro_cliente"
        st.rerun()

    if y.button("Consulta de Produtos", use_container_width=True):
        st.session_state["pagina"] = "consulta_produto"
        st.rerun()

    if y.button("Consulta de Dívida de Clientes", use_container_width=True):
        st.session_state["pagina"] = "consulta_divida"
        st.rerun()

    if y.button(
        "Atualizar Dívida de Clientes",
        use_container_width=True,
        disabled=not st.session_state["owner"],
    ):
        st.session_state["pagina"] = "atualizar_divida"
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state["autenticado"] = False
        st.session_state["pagina"] = "login"
        st.rerun()

    if st.sidebar.button("Support Page"):
        st.session_state["pagina"] = "suporte"
        st.rerun()
    if st.sidebar.button("My Account"):
        st.session_state["pagina"] = "conta"
        st.rerun()


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

else:
    # Se não estiver autenticado, ainda permite acesso à página de suporte
    if st.session_state["pagina"] == "support":
        page_support()
    elif st.session_state["pagina"] == "esqueci":
        esquci_senha()
    else:
        tela_login()
