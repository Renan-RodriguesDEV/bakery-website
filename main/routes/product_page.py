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
    st.markdown(
        "<h1 style='text-align: left; color: #DAA520;'>Consulta de Produtos</h1>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(
        [4, 1],
    )
    with col1.popover(
        "Consultar",
        use_container_width=True,
        help="Consulte um produto pelo nome",
        icon="🔍",
    ):
        nome = st.text_input(
            "Digite o nome do produto para consultar",
            key="nome_input",
            value="",
            label_visibility="collapsed",
        )
        produtos_select = search_product(nome)

        if st.button("Procurar produto", type="primary"):
            if produtos_select:
                produtos_select = DataFrame(produtos_select)
                produtos_select.drop("id", inplace=True, errors="ignore", axis=1)
                produtos_select["preco"] = produtos_select["preco"].map(
                    lambda x: f"R$ {x:.2f}".replace(".", ",")
                )
                produtos_select.columns = [
                    "Produto",
                    "Preço",
                    "Estoque",
                    "Categoria",
                ]
                st.table(produtos_select)
            else:
                st.error("Nenhum produto encontrado com esse nome")

    categoria = st.selectbox(
        "Selecione uma da(s) categoria(s)",
        ["categoria", "Bebidas", "Doces", "Salgados", "Padaria", "Mercearia"],
    )

    produtos = (
        select_all_products()
        if not categoria or categoria == "categoria"
        else select_all_products_by_category(categoria)
    )
    flag = True if produtos.empty else False
    df = DataFrame(produtos)
    df["Preço"] = df["Preço"].map(lambda x: f"R$ {x:.2f}".replace(".", ","))
    st.table(df)

    @st.cache_data
    def converter_df_to_excel(dataframe: DataFrame):
        buffer = io.BytesIO()
        dataframe.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer

    with col2:
        st.download_button(
            "Baixar planilha",
            icon="📁",
            data=converter_df_to_excel(produtos),
            file_name="produtos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            disabled=flag,
            help="Baixe a lista de produtos em formato de planilha excel",
            type="secondary",
            use_container_width=True,
        )
    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
