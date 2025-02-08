import io

import streamlit as st
from pandas import DataFrame
from src.models.repository.dataframes_repository import (
    select_all_products_by_category,
    select_all_products,
    search_product,
)


def consulta_produto():
    """Pagina para consulta de produtos"""
    st.title("Consulta de Produtos")
    categoria = st.selectbox(
        "Selecione uma da(s) categoria(s)",
        ["categoria", "Bebidas", "Doces", "Salgados", "Padaria", "Mercearia"],
    )
    print(categoria)

    produtos = (
        select_all_products()
        if not categoria or categoria == "categoria"
        else select_all_products_by_category(categoria)
    )
    print(categoria)
    flag = True if produtos.empty else False
    # Aqui você poderia listar os produtos cadastrados. Exemplo simples:
    st.table(produtos)
    nome = st.text_input("Digite o nome do produto para consultar")
    produtos_select = search_product(nome)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Consultar", type="primary"):
            if produtos_select:
                st.table(produtos_select)
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
            disabled=flag,
        )
    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
