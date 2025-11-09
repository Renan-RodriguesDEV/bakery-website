import streamlit as st
from src.models.repository.cart_repository import CartRepository
from src.models.repository.dataframes_repository import (
    select_all_products,
    select_all_products_by_category,
)
from src.models.repository.product_repository import ProductRepository
from src.models.repository.user_repository import UserRepository
from src.utils.uteis import Logger


def realizar_compra():
    """Pagina de compras a fazer"""
    st.title(":orange[Faça sua(s) Compra(s) 🛒]")
    df_produtos = select_all_products(
        limit=200,
    )
    cliente_session = st.session_state["username"]
    st.write(f"Cliente: {cliente_session}")
    categoria = st.selectbox(
        "Selecione uma da(s) categoria(s)",
        ["categoria", "Bebidas", "Doces", "Salgados", "Padaria", "Mercearia"],
    )
    print(categoria)
    produto = st.selectbox(
        "Selecione o produto",
        (
            df_produtos
            if not categoria or categoria == "categoria"
            else select_all_products_by_category(categoria)
        ),
    )
    preco = ProductRepository().select_product_price(produto)
    prod_objt = ProductRepository().select_product(produto)
    estoque = prod_objt.estoque if prod_objt else 0
    if estoque:
        quantidade = st.number_input(
            "Quantidade",
            value=1,
            min_value=1,
            step=1,
            max_value=estoque,
        )
    else:
        quantidade = 0
        st.warning("Produto fora de estoque")

    col1, col2 = st.columns([1, 1])

    if produto and preco:
        with st.container():
            preco_formatado = (
                f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )
            valor_total = preco * quantidade
            valor_total_formatado = (
                f"R$ {valor_total:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.html(
                f"""
                <div style="display:flex; flex-direction:column; gap:12px; padding:20px; border-radius:14px; background:#131313; border:1px solid #2b2b2b; box-shadow:0 6px 18px rgba(0,0,0,0.25);">
                    <div style="font-size:15px; color:#8B4513; font-weight:700; letter-spacing:0.5px; text-transform:uppercase;">
                        Resumo da compra
                    </div>

                    <div style="display:flex; flex-direction:column; background:#1b1b1b; border-radius:10px; padding:14px; border-left:4px solid #8B4513;">
                        <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:6px;">
                            <i class="fas fa-bread-slice" style="margin-right:6px;"></i>Produto selecionado
                        </div>
                        <div style="font-size:20px; font-weight:700; color:#f5f5f5;">{produto}</div>
                    </div>
                    
                    <div style="display:flex; flex-wrap:wrap; gap:12px;">
                        <div style="flex:1; min-width:180px; background:#1b1b1b; border-radius:10px; padding:14px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:8px;">
                                <i class="fas fa-tag" style="margin-right:6px;"></i>Preço unitário
                            </div>
                            <div style="font-size:20px; font-weight:700; color:#f5f5f5;">{preco_formatado}</div>
                        </div>
                        
                        <div style="flex:1; min-width:180px; background:#1b1b1b; border-radius:10px; padding:14px; border-left:4px solid #8B4513;">
                            <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:8px;">
                                <i class="fas fa-cubes" style="margin-right:6px;"></i>Quantidade
                            </div>
                            <div style="font-size:20px; font-weight:700; color:#f5f5f5;">{quantidade}</div>
                        </div>
                    </div>
                    
                    <div style="margin-top:6px; text-align:center;">
                        <div style="font-size:12px; color:#999; font-weight:600; margin-bottom:10px;">
                            <i class="fas fa-calculator" style="margin-right:6px;"></i>Valor final
                        </div>
                        <div style="display:inline-block; background:#1f2b1f; color:#4ade80; padding:12px 22px; border-radius:12px; font-size:24px; font-weight:800; box-shadow:0 4px 12px rgba(0,0,0,0.22);">
                            {valor_total_formatado}
                        </div>
                    </div>
                </div>
                
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                """
            )
        disable = True
        if col1.button(
            "Adicionar ao carrinho",
            icon=":material/add_shopping_cart:",
            type="primary",
            disabled=not estoque,
        ):
            cliente_obj = UserRepository().select_user(cliente_session, "Cliente")
            produto_obj = ProductRepository().select_product(produto)
            Logger.info(f"produto: {produto_obj}")
            Logger.info(f"cliente: {cliente_obj}")
            if produto_obj and cliente_obj:
                with CartRepository() as cart_repository:
                    cart_repository.add_to_cart(cliente_obj, produto_obj, quantidade)
                st.success(f" +{quantidade} {produto} adicionado ao carrinho 🛒")
                st.success(f" +{preco * quantidade} adicionado ao valor do carrinho 💵")
                disable = False
            else:
                st.error("Erro ao adicionar ao carrinho")
        if st.button(
            "Carrinho de Compras", icon=":material/shopping_cart:", disabled=disable
        ):
            st.session_state["pagina"] = "cart"
            st.rerun()

    if st.sidebar.button(
        "Home",
        icon=":material/home:",
        help="Ir para homepage",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["pagina"] = "homepage"
        st.rerun()
    if st.sidebar.button(
        "Consulta de produtos",
        use_container_width=True,
        type="primary",
        icon=":material/search:",
    ):
        st.session_state["pagina"] = "consulta_produto"
        st.rerun()
