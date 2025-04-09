from mail.mail_wrapper import NotifierMail
from notifier import Notifier
from spotify.spotify_wrapper import SpotifyFetch
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    spotify = SpotifyFetch()

    uri = spotify.get_uri_from_artist_name("eugene")
    if uri:
        disco = spotify.get_artist_discography(uri)

        max_album = max(disco)

    today = datetime.now().strftime("%d/%m/%Y")
    if max_album.release_date.strftime("%d/%m/%Y") >= today:
        notifier = Notifier()
        notifier.send_notification(max_album)
        mail_notifier = NotifierMail(os.getenv("MAIL_FROM"), os.getenv("MAIL_TO"))
        mail_notifier.send_notification(max_album)
    else:
        print("No released today..")


if __name__ == "__main__":
    main()
