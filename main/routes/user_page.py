import streamlit as st
from src.models.repository.dataframes_repository import select_all_clientes
from src.models.repository.user_repository import UserRepository
from src.utils.uteis import Logger, number_as_cpf, number_as_telephone, validate_email


def information():
    st.title("Informações de clientes")
    cliente = st.selectbox("Selecione o cliente", select_all_clientes())
    if st.button("Consultar", icon=":material/search:") and cliente:
        cliente_obj = None
        with UserRepository() as c:
            cliente_obj = c.select_user(cliente)
        if cliente_obj:
            st.subheader(f"Informações sobre: {cliente}")
            st.markdown(
                f"""
                <div style="background-color: #8B4513; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: white; margin-bottom: 15px;">Detalhes do Cliente</h3>
                    <div style="margin-left: 10px;">
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Nome:</strong> {cliente_obj.nome}</p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>CPF:</strong> {cliente_obj.cpf}</p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Telefone:</strong> <a href="https://wa.me/+55{cliente_obj.telefone}" style="color: #FFD700;">{cliente_obj.telefone}</a></p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Email:</strong> <a href="mailto:{cliente_obj.email}" style="color: #FFD700;">{cliente_obj.email}</a></p>
                        <p style="font-size: 16px; margin: 8px 0;"><strong>Status de ativação:</strong> <span style="color: #FFD700;">{cliente_obj.activate}</span></p>
                    </div>
                </div>
                <br></br>
                """,
                unsafe_allow_html=True,
            )
    if st.sidebar.button(
        "Home",
        icon=":material/home:",
        help="Ir para homepage",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["pagina"] = "homepage"
        st.rerun()


def my_account():
    if "autenticado" not in st.session_state or "usuario" not in st.session_state:
        st.error("Você precisa estar logado para ver sua conta")
        st.session_state["pagina"] = "login"
        st.rerun()
    else:
        Logger.sucess(f">>> Nome do usuario: {st.session_state['username']}")
        Logger.sucess(f">>> Tipo de usuario:{st.session_state['usuario']}")
        st.title("Minha Conta")
        user = st.session_state["username"]
        type_user = st.session_state["usuario"]
        user_data = UserRepository().select_user(user, type_user)
        x, y = st.columns([1, 1])
        if not user_data:
            st.error("Usuário não encontrado")
        else:
            if type_user == "Cliente":
                user_data = UserRepository().select_user(user, "Cliente")
                x.image(
                    "https://www.freeiconspng.com/uploads/head-icon-0.png",
                    width=100,
                    output_format="PNG",
                )
                x.write(f"Nome: {user_data.nome}")
                x.write(f"Email: {user_data.email}")
                x.write(f"CPF: {number_as_cpf(user_data.cpf)}")
                x.write(f"Telefone: {number_as_telephone(user_data.telefone)}")
                new_name = y.text_input(
                    "Nome: ", type="default", placeholder="Son Goku"
                )
                new_pswd = y.text_input("Senha: ", type="password", max_chars=11)
                new_email = y.text_input(
                    "Email: ", max_chars=100, placeholder="useremail@gmail.com"
                )
                new_telefone = y.text_input(
                    "Telefone: ", max_chars=15, placeholder="(21) 99999-9999"
                )
                new_cpf = y.text_input(
                    "CPF: ", max_chars=14, placeholder="666.666.666-69"
                )
                flag = False
                if new_name or new_pswd or new_email or new_telefone:
                    if not new_email:
                        flag = True
                    else:
                        if not validate_email(new_email):
                            flag = False
                            st.error("Email invalido")
                else:
                    flag = False
                    st.warning("Preencha algum dos campos para alteração")
                if y.button("Atualizar", type="primary"):
                    if flag:
                        with UserRepository() as u:
                            update = u.update_user(
                                user,
                                new_name,
                                new_pswd,
                                new_email,
                                new_cpf,
                                new_telefone,
                                type_user="Cliente",
                            )
                            if update:
                                st.success("Atualizado com sucesso")
                                st.success(
                                    "Aperte em voltar e depois faça o logout do usuario preenchendo com seus novos dados!!",
                                    icon="😁",
                                )
                            else:
                                st.error("Erro ao atualizar")

                    else:
                        st.error(
                            "É necessario preencher algum dos campos para atualizar"
                        )

            else:
                x.image(
                    "https://www.freeiconspng.com/uploads/head-icon-0.png",
                    width=100,
                    output_format="PNG",
                )
                x.write(f"Nome: {user_data.nome}")
                x.write(f"Email: {user_data.email}")
                new_name = y.text_input(
                    "Nome: ", type="default", placeholder="Son Goku"
                )
                new_pswd = y.text_input("Senha: ", type="password", max_chars=11)
                new_email = y.text_input(
                    "Email: ", max_chars=100, placeholder="useremail@gmail.com"
                )
                if new_name or new_pswd or new_email:
                    flag = True
                else:
                    flag = False
                    st.warning("Preencha algum dos campos para alteração")
                if y.button("Atualizar", type="primary"):
                    if flag:
                        with UserRepository() as u:
                            update = u.update_user(
                                user,
                                new_name,
                                new_pswd,
                                new_email,
                                type_user="Proprietario/Funcionario",
                            )
                            if update:
                                st.success("Atualizado com sucesso")
                                st.success(
                                    "Aperte em voltar e depois faça o logout do usuario preenchendo com seus novos dados!!",
                                    icon="😁",
                                )
                            else:
                                st.error("Erro ao atualizar")
                    else:
                        st.error(
                            "É necessario preencher algum dos campos para atualizar"
                        )

        if st.sidebar.button(
            "Home",
            icon=":material/home:",
            help="Ir para homepage",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "homepage"
            st.rerun()
