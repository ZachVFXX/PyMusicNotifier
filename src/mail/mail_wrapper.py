from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from dotenv import load_dotenv
from protocols import Album, User
import os
from jinja2 import Template

load_dotenv()


class NotifierMail:
    def __init__(
        self,
        mail_from: str = os.getenv("MAIL_FROM"),
        mail_to: str = os.getenv("MAIL_TO"),
        password_mail_from: str = os.getenv("MAIL_PASSWORD"),
        smtp_server: str = "smtp.gmail.com",
        port: int = 465,
    ):
        self.mail_from: str = mail_from
        self.password_mail_from: str = password_mail_from
        self.mail_to: str = mail_to
        self.smtp_server = smtp_server
        self.port = port

    def send_notification(self, albums: list[Album], user: User):
        with open("src/mail/mail_template.html", "r", encoding="utf-8") as file:
            html_template = file.read()

        album_data = []
        for album in albums:
            album_data.append(
                {
                    "artist_name": album.get_artists(),
                    "release_type": album.type,
                    "release_title": album.name,
                    "cover_url": album.image_url,
                    "release_date": album.release_date.to_date_string(),
                    "release_link": album.link,
                }
            )

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎵 {len(albums)} nouvelle(s) sortie(s) pour toi !"
        msg["From"] = self.mail_from
        msg["To"] = self.mail_to
        data = {
            "user_name": user.name,
            "albums": album_data,
            "unsubscribe_link": "https://tonapp.com/unsubscribe",
        }

        template = Template(html_template)
        html_content = template.render(**data)

        msg.attach(MIMEText(html_content, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.mail_from, self.password_mail_from)
            server.sendmail(self.mail_from, self.mail_to, msg.as_string())
            print("Email envoyé !")
