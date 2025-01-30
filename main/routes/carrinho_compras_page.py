import streamlit as st
from src.controller.payments import payment
from src.utils.uteis import Logger
from src.models.repository.cart_repository import CartRepository
from src.models.repository.product_repository import ProductRepository
from src.models.repository.user_repository import UserRepository


def shopping_cart():
    product_repository = ProductRepository()
    cart_repository = CartRepository()
    user_repository = UserRepository()
    user_session = st.session_state["username"]
    st.title(f"Bem vindo ao seu carrinho de compras :grey[{user_session}]")
    st.warning(
        "Após o pagamento retire seus produtos na loja!! após apertar em comprar seu carrinho será esvaziado"
    )
    selecionados = st.multiselect(
        "Selecione o que ira levar hoje!!!",
        [
            f" || ".join(
                [
                    f"item: {product_repository.select_product_by_id(carrinho.id_produto).nome}",
                    f"quantidade: {int(carrinho.quantidade)}",
                    f"valor total: R${int(carrinho.quantidade) * product_repository.select_product_by_id(carrinho.id_produto).preco}",
                ]
            )
            for carrinho in cart_repository.get_cart_by_user(
                user_repository.select_user(user_session, "Client").id
            )
        ],
    )
    col1, col2 = st.columns([1, 1])
    col1.html(
        """
<h4>Pague com pix e retire na hora <img src='https://img.icons8.com/?size=100&id=Dk4sj0EM4b20&format=png&color=000000' width='20'></img> </h4>

<p><b>Proprietario: </b> <span style='text-decoration: underline;'>Renan Rodrigues</span></p>
<p>Chave:</p>"""
    )
    col1.code("(19) 99872-2472")
    col1.html("<h4/>Banco Santander (SA)</h4>")
    selecionados_dict = {"produtos": [], "precos": [], "quantidades": []}
    for selecionado in selecionados:
        selecionados_dict["produtos"].append(
            selecionado.split(" || ")[0].split(": ")[1]
        )
        selecionados_dict["quantidades"].append(
            (int(selecionado.split(" || ")[1].split(": ")[1]))
        )
        selecionados_dict["precos"].append(
            float(selecionado.split(" || ")[2].split(": ")[1].replace("R$", ""))
        )

    col2.table([selecionado.split(" || ") for selecionado in selecionados])
    payment_link = ""

    if col2.button(
        "Comprar",
        type="primary",
        help="Clique para finalizar a compra pelo mercado pago",
        disabled=True if not selecionados else False,
    ):
        produtos = selecionados_dict["produtos"]
        precos = selecionados_dict["precos"]
        quantidades = selecionados_dict["quantidades"]

        if produtos and precos and quantidades:
            total_precos = sum(precos)
            payment_link = payment(" x ".join(produtos), total_precos, 1)
            Logger.info(f"link para pagamento {payment_link}")
            col2.success(f"link para pagamento {payment_link}")

        col2.html(
            f'<a href="{payment_link}" style="color:white; font-family:consolas; border: 2px solid green; border-radius: 12px; padding: 10px 20px; background-color: green; text-decoration: none;" target="_blank">Continuar pelo mercado pago</a>'
            if payment_link
            else None
        )
        for produto in produtos:
            cart_repository.remove_all_from_cart(
                user_repository.select_user(user_session, "Client").id,
                product_repository.select_product(produto).id,
            )
        Logger.warning("Produtos removidos !!")
    if st.button("Ir para home"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
