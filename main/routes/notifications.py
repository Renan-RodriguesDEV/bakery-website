import streamlit as st
from src.models.entities.database import Notifications
from src.models.repository.notifications_repository import NotificationsRepository


@st.dialog("Notificações 🔔")
def modal_notifications(
    unreads: list[Notifications], notifications_repository: NotificationsRepository
):
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
        for n in unreads:
            cols = st.columns([2, 2])
            cols[0].markdown(
                f"**{n.message}**  \n<small>{n.created_at.strftime('%d/%m/%Y %H:%M')}</small>",
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
