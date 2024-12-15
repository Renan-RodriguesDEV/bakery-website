import smtplib
from colorama import Fore, Style, init
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


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


def send_feedback_email(name, feedback):
    """Envia feedback por email

    Args:
        feedback (str): feedback a ser enviado
    """
    __USER = os.getenv("USER")
    __PASSWORD = os.getenv("PASSWORD")
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:
        Logger.log_blue("Conectando no servidor SMTP...")
        smtp.ehlo()
        # smtp.starttls()
        Logger.log_blue("Logando no servidor SMTP...")
        smtp.login(user=str(__USER), password=str(__PASSWORD))
        subject = "Feedback do site"
        body = f"Feedback de {name}: \n{feedback}"
        mensagem = MIMEText(body, "plain")
        mensagem["From"] = __USER
        mensagem["To"] = __USER
        mensagem["Subject"] = subject

        smtp.sendmail(
            from_addr=__USER,
            to_addrs=__USER,
            msg=mensagem.as_string(),
        )
        Logger.log_green(f"Feedback enviado com sucesso para o email {__USER}!")
