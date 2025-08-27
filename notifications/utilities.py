import os
import smtplib
from email.mime.text import MIMEText
from typing import Literal

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()


def check(stock=30, url=os.getenv("DATABASE_URL")):
    engine = create_engine(url, echo=True)
    session = sessionmaker(bind=engine)()
    with session.begin():
        result = session.execute(
            text("SELECT * FROM produtos WHERE estoque <= :stock"), {"stock": stock}
        )

        results = result.fetchall()

        results_dict = [dict(row._asdict()) for row in results]
        return results_dict


def notify(message, typed: Literal["warning", "danger"]):
    print(f"Notification sent: {message} - Type: {typed}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))

        subject = f"Notification - {str(typed).capitalize()}"
        body = message
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = os.getenv("EMAIL_RECIPIENT")

        smtp.sendmail(
            os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_RECIPIENT"), msg.as_string()
        )
