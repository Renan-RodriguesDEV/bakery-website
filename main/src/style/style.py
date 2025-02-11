import os
import streamlit as st


def sidebar_formatter():
    st.markdown(
        load_css("style.css"),
        unsafe_allow_html=True,
    )


def load_css(filename):
    with open(os.path.join(os.getcwd(), "main", "src", "style", filename), "r") as f:
        return f"<style>{f.read()}</style>"
