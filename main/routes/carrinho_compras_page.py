import pandas as pd
import streamlit as st
from src.models.repository.dividas_repository import register_sale
from src.controller.payments import get_payment_status, payment
from src.utils.uteis import Logger, generate_qr_code
from src.models.repository.cart_repository import CartRepository
from src.models.repository.product_repository import ProductRepository
from src.models.repository.user_repository import UserRepository
from src.models.configs.config_geral import configs


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
    select_all_checkbox = st.checkbox("Selecionar todos")
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
    with st.popover(
        "Selecione o que irá levar hoje!!!",
        icon="🛍️",
        help="Seleção de produtos",
        use_container_width=True,
    ):
        selecionados = []
        itens_options = []
        for item in itens_cart:
            itens_options.append(st.checkbox(item))
        for index, item in enumerate(itens_options):
            if item:
                selecionados.append(itens_cart[index])
        if select_all_checkbox:
            selecionados = [item for item in itens_cart]
    col1, col2 = st.columns([1, 1])
    col1.html(
        """
<h4>Pague com pix e retire na hora <img src='https://img.icons8.com/?size=100&id=Dk4sj0EM4b20&format=png&color=000000' width='20'></img> </h4>
"""
    )
    img = generate_qr_code(configs["pix_key"])
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
    print(df)
    col2.table(df) if not df.empty else None
    col2.markdown("---")
    col2.html(
        f"<p style='font-size:20px;color:darkgray;text-align:right'>Total: <span style='color:#DAA520'>R$ {sum(selecionados_dict['precos']):.2f}</span></p>".replace(
            ".", ","
        )
    )
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
            payment_link, payment_id = payment(" x ".join(produtos), total_precos, 1)
            Logger.info(f"link para pagamento {payment_link}")
            col2.success(f"link para pagamento gerado com sucesso!!", icon="🔓")

        (
            col2.markdown(
                f'<a href="{payment_link}" style="color:white; font-family:consolas; border: 2px solid green; border-radius: 12px; padding: 10px 20px; background-color: green; text-decoration: none;" target="_blank" rel="noopener noreferrer">Continuar pelo mercado pago</a>',
                unsafe_allow_html=True,
            )
            if payment_link
            else None
        )
        for produto in produtos:
            cart_repository.remove_all_from_cart(
                user_repository.select_user(user_session, "Cliente").id,
                product_repository.select_product(produto).id,
            )
        Logger.warning("Produtos removidos !!")

        # TODO: verificar se a compra foi realizada com sucesso na API do mercado pago

        for produto, qtde in zip(produtos, quantidades):
            register_sale(st.session_state["username"], produto, qtde)
            Logger.warning(
                f"Registrando venda para {st.session_state['username']} de {qtde} x {produto} do estoque"
            )

        # TODO: pós verificação, remover do estoque
        # else:
        #     for produto, qtde, precos in zip(produtos, quantidades):
        #         cart_repository.remove_from_stoke(produto, qtde)
        #         Logger.warning(f"Removendo {qtde} x {produto} do estoque")

    if st.sidebar.button("Ir para home", type="primary"):
        st.session_state["pagina"] = "homepage"
        st.rerun()
