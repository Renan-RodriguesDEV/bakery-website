import smtplib
from email.mime.text import MIMEText
from .uteis import Logger
from src.models.configs.config_geral import configs


class EmailSender:
    def __init__(self, usermail=configs["user"], password=configs["password"]):
        self.__USER = usermail
        self.__PASSWORD = password

    def send_feedback_email(self, name, feedback):
        """Envia feedback por email

        Args:
            feedback (str): feedback a ser enviado
        """

        with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:
            Logger.sucess("Conectando no servidor SMTP...")
            smtp.ehlo()
            # smtp.starttls()
            Logger.sucess("Logando no servidor SMTP...")
            smtp.login(user=str(self.__USER), password=str(self.__PASSWORD))
            subject = "Feedback do site"
            body = f"Feedback de {name}: \n{feedback}"
            mensagem = MIMEText(body, "plain")
            mensagem["From"] = self.__USER
            mensagem["To"] = self.__USER
            mensagem["Subject"] = subject

            smtp.sendmail(
                from_addr=self.__USER,
                to_addrs=self.__USER,
                msg=mensagem.as_string(),
            )
            Logger.info(f"Feedback enviado com sucesso para o email {self.__USER}!")

    def send_email(self, email, text, subject="Atenção, Padaria da Vila informa!!"):
        """Envia feedback por email

        Args:
            feedback (str): feedback a ser enviado
        """
        with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:
            Logger.sucess("Conectando no servidor SMTP...")
            smtp.ehlo()
            # smtp.starttls()
            Logger.sucess("Logando no servidor SMTP...")
            smtp.login(user=str(self.__USER), password=str(self.__PASSWORD))
            subject = subject
            body = f"""
<div><i>Olá {email}, </i></div>
<div>{text}</div>"""
            mensagem = MIMEText(body, _subtype="html")
            mensagem["From"] = self.__USER
            mensagem["To"] = email
            mensagem["Subject"] = subject

            smtp.sendmail(
                from_addr=self.__USER,
                to_addrs=email,
                msg=mensagem.as_string(),
            )
            Logger.info(f"Email enviado com sucesso para o email {email}!")
