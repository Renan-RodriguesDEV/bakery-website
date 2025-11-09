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
            telefone_limpo = "".join(
                filter(str.isdigit, str(cliente_obj.telefone or ""))
            )
            st.html(
                f"""
                <div style="display:flex; flex-direction:column; gap:16px; padding:24px; border-radius:16px; background:#131313; border:1px solid #2b2b2b; box-shadow:0 8px 24px rgba(0,0,0,0.35); color:#f5f5f5;">
                    <div style="font-size:15px; color:#d4a373; font-weight:700; letter-spacing:0.6px; text-transform:uppercase;">
                        Detalhes do cliente
                    </div>
                    <div style="display:grid; gap:14px; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));">
                        <div style="background:#1b1b1b; border-radius:12px; padding:16px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:6px;">
                                <i class="fas fa-user" style="margin-right:6px;"></i>Nome
                            </div>
                            <div style="font-size:18px; font-weight:700;">{cliente_obj.nome}</div>
                        </div>
                        <div style="background:#1b1b1b; border-radius:12px; padding:16px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:6px;">
                                <i class="fas fa-id-card" style="margin-right:6px;"></i>CPF
                            </div>
                            <div style="font-size:18px; font-weight:700;">{number_as_cpf(cliente_obj.cpf)}</div>
                        </div>
                        <div style="background:#1b1b1b; border-radius:12px; padding:16px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:6px;">
                                <i class="fas fa-phone" style="margin-right:6px;"></i>Telefone
                            </div>
                            <a href="https://wa.me/55{telefone_limpo}" style="display:inline-flex; align-items:center; gap:6px; font-size:18px; font-weight:700; color:#4ade80; text-decoration:none;">
                                {number_as_telephone(cliente_obj.telefone)}
                                <i class="fas fa-arrow-up-right-from-square" style="font-size:14px;"></i>
                            </a>
                        </div>
                        <div style="background:#1b1b1b; border-radius:12px; padding:16px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:6px;">
                                <i class="fas fa-envelope" style="margin-right:6px;"></i>Email
                            </div>
                            <a href="mailto:{cliente_obj.email}" style="display:block; font-size:18px; font-weight:700; color:#93c5fd; text-decoration:none; overflow-wrap:anywhere; word-break:break-word;">
                                {cliente_obj.email}
                            </a>
                        </div>
                        <div style="background:#1b1b1b; border-radius:12px; padding:16px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:6px;">
                                <i class="fas fa-toggle-on" style="margin-right:6px;"></i>Status de ativação
                            </div>
                            <div style="display:inline-flex; align-items:center; gap:8px; padding:6px 14px; border-radius:999px; background:#1f2b1f; color:#4ade80; font-size:14px; font-weight:700;">
                                <span style="width:8px; height:8px; border-radius:50%; background:#4ade80;"></span>
                                {cliente_obj.activate}
                            </div>
                        </div>
                    </div>
                </div>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                """
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
                                new_email.strip(),
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
                                new_email.strip(),
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
