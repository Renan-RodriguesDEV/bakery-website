import telebot
import os
from dotenv import load_dotenv

from src.models.repository.product_repository import ProductRepository


load_dotenv()


_TOKEN = os.getenv("TOKEN_TELEGRAM")
print(_TOKEN)
_bot = telebot.TeleBot(_TOKEN)


@_bot.message_handler(commands=["start"])
def start(message):
    _bot.reply_to(
        message,
        """Site referente ao nosso sistema:
http://localhost:8501/
""",
    )


@_bot.message_handler(commands=["contato"])
def contato(message):
    msg = _bot.reply_to(
        message,
        """Obrigado por entrar em contato conosco!! links para mais informações abixo.""",
    )

    _bot.send_message(
        msg.chat.id,
        text="""Nosso site: http://localhost:8501/
Gmail: renanrodrigues7110@gmail.com""",
    )
    _bot.send_contact(
        msg.chat.id,
        phone_number="5519998722472",
        first_name="Renan",
        last_name="Rodrigues",
    )


@_bot.message_handler(commands=["produtos"])
def produtos(message):
    with ProductRepository() as p:
        produtos = p.select_all_products()
        if not produtos:
            _bot.reply_to(message, "Nenhum produto cadastrado.")
            return

        lista_formatada = "\n".join(
            f"• {prod.nome} - R$ {prod.preco}" for prod in produtos
        )
        _bot.reply_to(message, f"Lista de produtos:\n{lista_formatada}")


@_bot.message_handler(func=lambda message: True)
def hello(message):
    _bot.reply_to(
        message,
        """Olá, eu sou o bot do sistema de vendas. Como posso te ajudar?
/produtos (veja nossa lista de produtos e preços!!)
/contato (entre em contato conosco)
/start (site referente ao nosso sistema)
                """,
    )


def start_bot():
    try:
        _bot.infinity_polling()
    except Exception as e:
        print(f"[ERROR] >>> {str(e)} <<< [ERROR]")
