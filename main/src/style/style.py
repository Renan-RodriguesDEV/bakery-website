import os
import streamlit as st

def load_css(filename):
    with open(
        os.path.join(os.getcwd(), "main", "src", "style", "components", filename), "r"
    ) as f:
        st.html(f"<style>{f.read()}</style>")
