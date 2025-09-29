import streamlit as st
from src.chatbot.chatbot import ask_chat


@st.dialog("AI Assistant")
def show_chatbot_modal():
    # garante histórico
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.markdown("Converse com a assistente da padaria.")

    # mostra histórico
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # input
    user_input = st.chat_input("Digite sua mensagem...")

    if user_input:
        # adiciona usuário
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # resposta IA
        with st.chat_message("assistant"):
            with st.spinner("Pensando...", show_time=True):
                resposta = ask_chat(user_input)  # garantir que retorna str
                st.markdown(
                    f"{resposta.get('message')}\n\nFontes: {resposta.get('font')}"
                )

        # salva resposta IA
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": resposta.get("message")}
        )
