import pandas as pd
import streamlit as st
from src.controller.payments import payment
from src.utils.uteis import Logger, generate_qr_code
from src.models.repository.cart_repository import CartRepository
from src.models.repository.product_repository import ProductRepository
from src.models.repository.user_repository import UserRepository


def shopping_cart():
    """Pagina do carrinho de compras"""
    product_repository = ProductRepository()
    cart_repository = CartRepository()
    user_repository = UserRepository()
    user_session = st.session_state["nome_de_sessao"]
    st.html(
        f"<h4 style='color:darkgray;font-size:30px'>Bem vindo ao seu carrinho de compras <span style='color:#DAA520'>{user_session}</span><h4>"
    )
    st.warning(
        "Após o pagamento retire seus produtos na loja!! após apertar em comprar seu carrinho será esvaziado"
    )
    checkbox = st.checkbox("Selecionar todos")
    itens_cart = [
        f" ➕ ".join(
            [
                f"item: {product_repository.select_product_by_id(carrinho.id_produto).nome}",
                f"quantidade: {int(carrinho.quantidade)}",
                f"valor total: R${int(carrinho.quantidade) * product_repository.select_product_by_id(carrinho.id_produto).preco}",
            ]
        )
        for carrinho in cart_repository.get_cart_by_user(
            user_repository.select_user(user_session, "Cliente").id
        )
    ]
    print(checkbox)
    selecionados = st.multiselect(
        "Selecione o que ira levar hoje!!!",
        itens_cart,
        default=itens_cart if checkbox else None,
    )
    col1, col2 = st.columns([1, 1])
    col1.html(
        """
<h4>Pague com pix e retire na hora <img src='https://img.icons8.com/?size=100&id=Dk4sj0EM4b20&format=png&color=000000' width='20'></img> </h4>
"""
    )
    img = generate_qr_code(st.secrets["PIX_KEY"])
    col1.image(
        img,
        caption="Escaneie o QRcode para realizar o pagamento no mercado pago!!",
        width=350,
    )
    col1.html(
        """<h4/>Se preferir prossiga com a chave abaixo para o Santander (S/A)<p style='color:#DAA520'>Renan Rodrigues, AG: 0483<p/><h4>"""
    )
    col1.code(
        """(19) 99872-2472""",
        language="python",
    )
    selecionados_dict = {"produtos": [], "precos": [], "quantidades": []}
    for selecionado in selecionados:
        selecionados_dict["produtos"].append(
            selecionado.split(" ➕ ")[0].split(": ")[1]
        )
        selecionados_dict["quantidades"].append(
            (int(selecionado.split(" ➕ ")[1].split(": ")[1]))
        )
        selecionados_dict["precos"].append(
            float(selecionado.split(" ➕ ")[2].split(": ")[1].replace("R$", ""))
        )
    df = pd.DataFrame(
        {
            "Produto": selecionados_dict["produtos"],
            "Quantidade": selecionados_dict["quantidades"],
            "Valor": [
                f"R$ {preco:.2f}".replace(".", ",")
                for preco in selecionados_dict["precos"]
            ],
        }
    )
    col2.table(df)
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
                user_repository.select_user(user_session, "Cliente").id,
                product_repository.select_product(produto).id,
            )
        Logger.warning("Produtos removidos !!")
    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
