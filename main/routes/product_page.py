import io

import streamlit as st
from pandas import DataFrame
from src.models.repository.dataframes_repository import (
    search_product,
    select_all_products,
    select_all_products_by_category,
)


def consulta_produto():
    """Pagina para consulta de produtos"""
    cols = st.sidebar.columns([2, 2, 2], vertical_alignment="center")
    items_per_page = cols[0].slider(
        "Itens por página",
        max_value=100,
        min_value=10,
        value=10,
        step=2,
        help="Selecione o número de itens por página",
    )
    # current_page = cols[2].number_input("Pagina", min_value=1, step=1, max_value=100)
    preco_min = cols[0].number_input("Valor Min.", min_value=0, max_value=500)
    preco_max = cols[0].number_input(
        "Valor Max.", min_value=0, max_value=500, value=500
    )
    filter_by = cols[2].selectbox("Ordenar por", ["nome", "preco", "estoque"])
    filter_order_by = cols[2].selectbox(
        "Ordem",
        [
            "maior",
            "menor",
        ],
    )
    produtos = select_all_products(
        limit=items_per_page,
        by=filter_by,
        asc=(filter_order_by == "menor"),
    )

    if preco_min != 0.0 or preco_max != 1000.0:
        produtos = produtos[
            (produtos["Preço"] >= preco_min) & (produtos["Preço"] <= preco_max)
        ]
    st.html(
        """
    <style>
        .custom-header {
            background-color: #1e1e1e;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-bottom: 25px;
            border: 1px solid #333;
            transition: all 0.3s ease;
        }
        .custom-header:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            transform: translateY(-2px);
        }
        .custom-header h1 {
            color: #DAA520;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 600;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        @media (max-width: 768px) {
            .custom-header {
                padding: 20px;
            }
            .custom-header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
    <div class="custom-header">
        <h1>Consulta de Produtos</h1>
    </div>
    """,
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
        produtos_select = None

        if st.button("Procurar produto", type="primary"):
            if nome.strip():
                produtos_select = search_product(nome.strip())
            if produtos_select is not None and not produtos_select.empty:
                produtos_select = DataFrame(produtos_select)
                produtos_select.drop("id", inplace=True, errors="ignore", axis=1)

                # Verificar se a coluna 'preco' existe antes de acessá-la
                if "preco" in produtos_select.columns:
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
    if categoria and categoria != "categoria":
        produtos = select_all_products_by_category(
            categoria,
            limit=items_per_page,
            by=filter_by,
            asc=(filter_order_by == "menor"),
        )
        produtos = produtos[
            (produtos["Preço"] >= preco_min) & (produtos["Preço"] <= preco_max)
        ]

    flag = True if produtos.empty else False
    df = DataFrame(produtos)
    df["Preço"] = df["Preço"].map(lambda x: f"R$ {x:.2f}".replace(".", ","))
    if not produtos.empty:
        st.table(df)
    else:
        st.warning("Nenhum produto encontrado!!")

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
    if st.sidebar.button(
        "Home",
        icon=":material/home:",
        help="Ir para homepage",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["pagina"] = "homepage"
        st.rerun()

    if st.session_state["owner"]:
        if st.sidebar.button(
            "Editar Produtos",
            icon=":material/edit:",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "cadastro_produto"
            st.rerun()
    else:
        if st.sidebar.button(
            "Comprar",
            icon=":material/add_shopping_cart:",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "realizar_compra"
            st.rerun()
