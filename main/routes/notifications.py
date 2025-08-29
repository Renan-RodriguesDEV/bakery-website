import streamlit as st
from src.models.repository.notifications_repository import NotificationsRepository


@st.dialog("notifications")
def modal_notifications(unread, notifications_repository: NotificationsRepository):
    if not unread:
        st.info("Nenhuma notificação nova.")
    else:
        to_mark = []
        for n in unread:
            cols = st.columns([2, 2])
            cols[0].markdown(
                f"**{n.message}**  \n<small>{n.created_at}</small>",
                unsafe_allow_html=True,
            )
            if cols[1].button("Marcar lida", key=f"read_{n.id}"):
                to_mark.append(n.id)
        if to_mark:
            for n_id in to_mark:
                notifications_repository.mark_as_read(n_id)
            st.rerun()
