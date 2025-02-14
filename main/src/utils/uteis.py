import secrets
import time
import qrcode
import io
from colorama import Fore, Style, init


class Logger:

    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def info(text):
        """Faz logs de texto na cor verde

        Args:
            text (str): texto a ser exibido na cor verde
        """
        print(
            f"{time.strftime('%X')} {Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}"
        )

    @staticmethod
    def warning(text):
        """Faz logs de texto na cor verde

        Args:
            text (str): texto a ser exibido na cor verde
        """
        print(
            f"{time.strftime('%X')} {Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}"
        )

    @staticmethod
    def sucess(text):
        """Faz logs de texto na cor azul

        Args:
            text (str): texto a ser exibido na cor azul
        """
        print(f"{time.strftime('%X')} {Style.BRIGHT}{Fore.BLUE}{text}{Style.RESET_ALL}")

    @staticmethod
    def error(text):
        """Faz logs de texto na cor vermelho

        Args:
            text (str): texto a ser exibido na cor vermelho
        """
        print(f"{time.strftime('%X')} {Style.BRIGHT}{Fore.RED}{text}{Style.RESET_ALL}")


def generate_token():
    while True:
        token = secrets.token_urlsafe(8)
        if len(token) == 11:
            return token


def str_as_number(string: str):
    string = (
        string.replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")
        .replace("+", "")
    )
    return string.strip()


def number_as_telephone(string: str):
    # Verificar e garantir antens se tá numerico
    string = str_as_number(string)
    if len(string) == 11:
        return f"({string[0:2]}) {string[2:7]}-{string[7:]}"
    return string


def number_as_cpf(string: str):
    # Verificar e garantir antens se tá numerico
    string = str_as_number(string)
    if len(string) == 11:
        return f"{time.strftime('%X')} {string[0:3]}.{string[3:6]}.{string[6:9]}-{string[9:]}"
    return string


def validate_email(email: str):
    if "@" in email and not email.startswith("@") and not email.endswith("@"):
        return True
    return False


def generate_qr_code(data):
    """Gera um QR code a partir de uma string"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Converte a imagem para bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return img_byte_arr
