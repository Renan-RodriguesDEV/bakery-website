import streamlit as st
from src.models.repository.notifications_repository import notifications_repository


def get_unreads():
    return notifications_repository.get_unread_notifications()


@st.dialog("Notificações 🔔")
def modal_notifications(notifications_repository):
    unreads = get_unreads()
    if not unreads:
        st.info("Nenhuma notificação nova.")
    else:
        to_mark = []
        if st.button(
            "Marcar todas como lidas",
            icon=":material/mark_chat_read:",
        ):
            for unread in unreads:
                notifications_repository.mark_as_read(unread.id)
                if "unreads" in st.session_state:
                    del st.session_state["unreads"]
                if "count_unread" in st.session_state:
                    del st.session_state["count_unread"]
        for n in unreads:
            cols = st.columns([2, 2])
            cols[0].markdown(
                f"""
                <div style="padding: 10px; border-left: 4px solid #4CAF50; background-color: #f9f9f9; margin-bottom: 10px;">
                    <strong style="color: #333;">{n.message}</strong><br>
                    <small style="color: #666;">{n.created_at.strftime("%d/%m/%Y %H:%M")}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if cols[1].button(
                "",
                key=f"read_{n.id}",
                icon=":material/done_all:",
                help="Marcar como lida",
            ):
                to_mark.append(n.id)

        if to_mark:
            for n_id in to_mark:
                notifications_repository.mark_as_read(n_id)
                st.success("Notificação marcada como lida.")
