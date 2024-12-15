import io
from pandas import DataFrame
import streamlit as st
from src.utils.uteis import *
from src.controller.payments import payment
from src.models.entities.database import *
from src.models.repository.database_repository import *

Logger.log_green("[==] Runnig server streamlit localhost [==]")
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


# Função para a tela de login
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
    if st.button("Login", type="primary"):
        if autenticar_usuario(username, password, type_user=tipo_user):
            st.session_state["autenticado"] = True
            st.session_state["owner"] = True if tipo_user == "Owner/Employee" else False
            st.session_state["usuario"] = username
            st.session_state["pagina"] = "homepage"  # Redireciona para a homepage
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")


# Função para enviar feedback
@st.cache_data
def send_feedback(feedback):
    send_feedback_email(str(st.session_state["usuario"]), feedback)
    st.success(f"Feedback enviado com sucesso: {st.session_state['usuario']}")


# Função para a homepage
def homepage():
    st.title(f"Bem-vindo, :gray[{st.session_state['usuario']}!]")
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


# Função para o cadastro de produtos
def cadastro_produto():
    st.title(":gray[Cadastro]/:red[Deleção] de Produtos")
    selection = st.selectbox("Selecione a ação", ["Cadastro", "Deleção"])
    if selection == "Cadastro":
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        qtde = st.number_input("Quantidade", min_value=0, step=1)

        if st.button("Cadastrar Produto", type="primary"):
            register_product(nome, float(preco), int(qtde))
            st.success(f"Produto {nome} cadastrado com sucesso!")
    else:
        produto = st.selectbox("Selecione o produto", select_all_produtos())
        Logger.log_green(produto)
        if st.button("Deletar Produto", type="primary"):
            deletion = delete_product(produto)
            if deletion:
                st.success(f"Produto {produto} deletado com sucesso!")
            else:
                st.error(f"Não foi possivel apagar o produto")
    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para o cadastro de clientes
def cadastro_cliente():
    st.title(":gray[Cadastro]/:red[Deleção] de Clientes")
    action = st.selectbox("Selecione a ação", ["Cadastro", "Deleção"])
    if action == "Cadastro":
        nome = st.text_input("Nome do Cliente")
        cpf = st.text_input("CPF do Cliente", placeholder="123.456.789-00")
        email = st.text_input("Email do Cliente", placeholder="darkside@gmail.com")
        telefone = st.text_input("Telefone do Cliente")

        if st.button("Cadastrar Cliente", type="primary"):
            cpf = cpf.replace(".", "").replace("-", "")
            register_client(nome, cpf, telefone, email)
            st.success(f"Cliente {nome} cadastrado com sucesso!")
    else:
        cliente = st.selectbox("Selecione o cliente", select_all_clientes())
        if st.button("Deletar Cliente", type="primary"):
            Logger.log_green(f"Cliente a deletar: {cliente}")
            deletion = delete_client(cliente)
            if deletion:
                st.success(f"Cliente {cliente} deletado com sucesso!")
            else:
                st.error(f"Não foi possivel apagar o cliente")
    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de produtos
def consulta_produto():
    st.title("Consulta de Produtos")
    produtos = select_all_produtos()
    # Aqui você poderia listar os produtos cadastrados. Exemplo simples:
    st.table(produtos)
    nome = st.text_input("Digite o nome do produto para consultar")
    produto = select_product_by_name(nome)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Consultar", type="primary"):
            if produto.shape[0] > 0:
                st.write(produto)
            else:
                st.error("Nenhum produto encontrado com esse nome")

    @st.cache_data
    def converter_df_to_excel(dataframe: DataFrame):
        buffer = io.BytesIO()
        dataframe.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer

    with col2:
        st.download_button(
            "Download produtos",
            data=converter_df_to_excel(produtos),
            file_name="produtos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de dívida de clientes
def consulta_divida():

    @st.cache_data
    def converter_df_to_excel(dataframe: DataFrame):
        try:
            buffer = io.BytesIO()
            dataframe.to_excel(buffer, index=False)
            buffer.seek(0)
            return buffer
        except Exception as e:
            st.warning(f"Não há cliente e produtos existentes na base de dados")
            pass

    if st.session_state["owner"]:
        st.title("Consulta de Dívida de Clientes")
        # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
        df_clientes = select_all_clientes()

        cliente = st.selectbox(
            "Selecione o cliente",
            df_clientes["nome"].to_list(),
        )
        divida = select_debt_by_client(cliente)
        st.subheader(f"Divida do cliente :gray[{cliente}]", divider="red")
        st.write(
            f"""<p style="font-size:30px;">Valor atual: <span style="text-decoration:underline; color:green; font-weight:bold;">R$ {divida if divida else 0.00}</span></p>""",
            unsafe_allow_html=True,
        )

        if st.button("Consulta completa", type="primary"):
            st.table(select_all_sales_by_client(cliente))
        try:
            st.download_button(
                label="Download divida",
                data=converter_df_to_excel(select_all_sales_by_client(cliente)),
                file_name="divida.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
            )
        except Exception as e:
            st.button(f"Dowload divida", disabled=True)
            pass
        if st.button("Voltar"):
            st.session_state["pagina"] = "homepage"
            st.rerun()
    else:
        st.title("Consulta de Dívida de Clientes")

        with st.form(key="consulta_form"):
            cliente = st.text_input(
                "Nome completo", help="Digite o nome completo como no cadastro"
            )
            cpf = st.text_input(
                "CPF",
                help="Digite seu cpf completo como no cadastro, sem caracteres",
                max_chars=11,
                placeholder="123.456.789-00",
            )
            consultar = st.form_submit_button("Consultar")

        if consultar:
            divida = select_debt_by_client(cliente, cpf)
            st.write(f"Divida do cliente {cliente}: R$ {divida if divida else 0.00}")
            divida_total = select_all_sales_by_client(cliente)
            if divida_total is not None:
                st.table(divida_total)
                st.download_button(
                    label="Download divida",
                    data=converter_df_to_excel(select_all_sales_by_client(cliente)),
                    file_name="divida.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.error("Nenhum cliente encontrado com esse nome")

        if st.button("Voltar"):
            st.session_state["pagina"] = "homepage"
            st.rerun()


def atualizar_divida():
    st.title("Atualizar Dívida de Clientes")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_clientes = select_all_clientes()
    df_produtos = select_all_produtos()
    cliente = st.selectbox("Selecione o cliente", df_clientes["nome"].to_list())
    action = st.selectbox("Adicionar/Remover divida", ["Adicionar", "Remover"])
    if action == "Adicionar":
        produto = st.selectbox("Selecione o produto", df_produtos)
        preco = None
        try:
            preco = select_price_by_name(produto)["preco"]
        except Exception as e:
            st.warning("Produto não encontrado")
            pass
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        st.markdown(
            f"<span style='font-size:30px; text-decoration:underline; font-family:JetBrains mono'>Valor final: :green[${preco * quantidade if (preco and quantidade)!=None else 0}]</span>",
            unsafe_allow_html=True,
        )
        if st.button("Atualizar"):

            is_register = register_sale(cliente, produto, quantidade)
            if is_register:
                st.success(
                    f"Venda registrada com sucesso no valor de R${preco*quantidade}!"
                )
            else:
                st.error("Erro ao registrar a venda")
    else:
        divida_total = select_debt_by_client(cliente)
        st.write(
            f"**O cliente :blue[{cliente}] tem a divida total no valor: :gray[R${divida_total}]**"
        )

        st.warning("Cuidado ao remover a divida, essa ação não pode ser desfeita")
        if st.button(
            "Zerar divida",
            type="primary",
            help="Atenção, essa ação não pode ser desfeita",
        ):
            is_pag = update_divida(cliente)
            if is_pag:
                st.success(
                    f"Pagamento registrado com sucesso!! a conta atual está em R$ 0,00"
                )
            else:
                st.error("Erro ao registrar a pagamento")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para realizar a compra
def realizar_compra():
    st.title("Realizar Compra")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_produtos = select_all_produtos()
    cliente = st.session_state["usuario"]
    st.write(f"Cliente: {cliente}")
    produto = st.selectbox("Selecione o produto", df_produtos)
    preco = select_price_by_name(produto)["preco"]
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    st.markdown(
        f"""
        \n:green[PRODUTO]: **{produto}** 
        \n:green[PREÇO UNITÁRIO]: **`R$`{preco}** 
        \n:green[VALOR FINAL]: **`R$`{preco*quantidade}**""",
        unsafe_allow_html=True,
    )
    if st.button("Comprar", type="primary"):
        try:
            link_paryment = payment(str(produto), float(preco), int(quantidade))
            Logger.log_blue(f"link para pagamento {link_paryment}")
            # Redireciona automaticamente
            st.page_link(
                page=link_paryment, label=":green[Ir para o Pagamento]", icon="💸"
            )

            st.success(f"Venda registrada com sucesso no valor de {preco*quantidade}!")
        except Exception as e:
            st.error("Erro ao registrar a venda")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Configurando a sessão para manter o estado do login e da página
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"  # Define a página inicial como login
# Inicializa "owner" com False por padrão, caso ainda não tenha sido definido
if "owner" not in st.session_state:
    st.session_state["owner"] = False
# Verifica se o usuário está autenticado
if st.session_state["autenticado"]:
    # Navega entre as páginas com base no estado
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
else:
    tela_login()
