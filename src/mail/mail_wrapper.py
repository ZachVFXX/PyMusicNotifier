from email.message import EmailMessage
import smtplib
import ssl


from dotenv import load_dotenv

from protocols import Album
import os

load_dotenv()


class NotifierMail:
    def __init__(
        self,
        mail_from: str,
        mail_to: str,
        password_mail_from: str = os.getenv("MAIL_PASSWORD"),
        smtp_server: str = "smtp.gmail.com",
        port: int = 465,
    ):
        self.mail_from: str = mail_from
        self.password_mail_from: str = password_mail_from
        self.mail_to: str = mail_to
        self.smtp_server = smtp_server
        self.port = port

    def send_notification(self, album: Album):
        msg = EmailMessage()
        msg["Subject"] = f"A new {album.type} is release !"
        msg["From"] = self.mail_from
        msg["To"] = self.mail_to
        msg.set_content(
            f"A new {album.type} is release by {album.get_artists()}. \nIts name is {album.name}, release on {album.release_date.strftime('%d/%m/%Y')}"
        )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.mail_from, self.password_mail_from)
            print(server.sendmail(self.mail_from, self.mail_to, msg.as_string()))
