import secrets
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
        print(f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}")

    @staticmethod
    def warning(text):
        """Faz logs de texto na cor verde

        Args:
            text (str): texto a ser exibido na cor verde
        """
        print(f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}")

    @staticmethod
    def sucess(text):
        """Faz logs de texto na cor azul

        Args:
            text (str): texto a ser exibido na cor azul
        """
        print(f"{Style.BRIGHT}{Fore.BLUE}{text}{Style.RESET_ALL}")

    @staticmethod
    def error(text):
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


def str_as_number(string: str):
    string = string.replace("-", "").replace("(", "").replace(")", "").replace(".", "")
    return string.strip()


def number_as_telephone(string: str):
    # First clean the string to ensure only numbers
    string = str_as_number(string)
    # Format: (11) 99752-6985
    if len(string) == 11:
        return f"({string[0:2]}) {string[2:7]}-{string[7:]}"
    elif len(string) == 10:
        return f"({string[0:2]}) {string[2:6]}-{string[6:]}"
    return string


def number_as_cpf(string: str):
    # First clean the string to ensure only numbers
    string = str_as_number(string)
    # Format: 444.888.999-30
    if len(string) == 11:
        return f"{string[0:3]}.{string[3:6]}.{string[6:9]}-{string[9:]}"
    return string
