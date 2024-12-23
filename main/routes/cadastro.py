import streamlit as st
from src.models.repository.product_repository import ProductRepository
from src.models.repository.user_repository import UserRepository
from src.utils.uteis import Logger
from src.models.repository.database_repository import (
    select_all_clientes,
    select_all_produtos,
)


# Função para o cadastro de produtos
def cadastro_produto():
    st.title(":gray[Cadastro]/:red[Deleção] de Produtos")
    selection = st.selectbox("Selecione a ação", ["Cadastro", "Deleção"])
    if selection == "Cadastro":
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        qtde = st.number_input("Quantidade", min_value=0, step=1)

        if st.button("Cadastrar Produto", type="primary"):
            ProductRepository().insert_product(nome, float(preco), int(qtde))
            st.success(f"Produto {nome} cadastrado com sucesso!")
    else:
        produto = st.selectbox("Selecione o produto", select_all_produtos())
        Logger.log_green(produto)
        if st.button("Deletar Produto", type="primary"):
            deletion = ProductRepository().delete_product(produto)
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
            cadasto = UserRepository().insert_user(
                username=nome,
                cpf=cpf,
                telefone=telefone,
                email=email,
                type_user="Client",
            )
            if cadasto:
                st.success(f"Cliente {nome} cadastrado com sucesso!")
            else:
                st.error(f"Não foi possivel cadastrar o cliente")
    else:
        cliente = st.selectbox("Selecione o cliente", select_all_clientes())
        if st.button("Deletar Cliente", type="primary"):
            Logger.log_green(f"Cliente a deletar: {cliente}")
            deletion = UserRepository().delete_user(cliente, "Client")
            if deletion:
                st.success(f"Cliente {cliente} deletado com sucesso!")
            else:
                st.error(f"Não foi possivel apagar o cliente")
    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
