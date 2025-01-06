import smtplib
from email.mime.text import MIMEText
from streamlit import secrets
from .uteis import Logger


class EmailSender:
    def __init__(self, usermail=secrets["USER"], password=secrets["PASSWORD"]):
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

    def send_email(self, email, text):
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
            subject = "Reset Token WebAppBakary"
            body = f"<p>Olá {email}, esse é o seu <b>reset-token</b></p><p>{text}<p>"
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
