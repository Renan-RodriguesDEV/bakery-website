import secrets
from colorama import Fore, Style, init


class Logger:

    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def log_green(text):
        """Faz logs de texto na cor verde

        Args:
            text (str): texto a ser exibido na cor verde
        """
        print(f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}")

    @staticmethod
    def log_blue(text):
        """Faz logs de texto na cor azul

        Args:
            text (str): texto a ser exibido na cor azul
        """
        print(f"{Style.BRIGHT}{Fore.BLUE}{text}{Style.RESET_ALL}")

    @staticmethod
    def log_red(text):
        """Faz logs de texto na cor vermelho

        Args:
            text (str): texto a ser exibido na cor vermelho
        """
        print(f"{Style.BRIGHT}{Fore.RED}{text}{Style.RESET_ALL}")


def generate_token():
    while True:
        token = secrets.token_urlsafe(8)  # Using smaller input to get ~11 chars
        if len(token) == 11:
            return token
