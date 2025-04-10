from dotenv import load_dotenv
import pendulum
from mail.mail_wrapper import NotifierMail
from notifier import Notifier
from protocols import Album, Fetch, Sender, User

from soundclouds.soundcloud_wrapper import SoundCloudFetch
from spotify.spotify_wrapper import SpotifyFetch

load_dotenv()


class MusicNotifier:
    def __init__(self, period_to_fetch: int = 1):
        self.period_to_fetch = period_to_fetch
        self.list_of_new_album: list[Album] = []
        self.user: User | None = None

    def fetch(self, artists: list[str], fetcher: list[Fetch]) -> None:
        self.user = fetcher[0].get_username()
        for artist in artists:
            for fetch in fetcher:
                print(f"Fetching {artist} with {fetch}")
                album: Album = fetch.get_last_album_from_artist(artist)
                if album:
                    today = pendulum.today().subtract(days=self.period_to_fetch)
                    if album.release_date >= today:
                        print(f"New {album.type} by {artist}: {album.name}")
                        self.list_of_new_album.append(album)

    def send(self, senders: list[Sender]) -> None:
        send_album = []
        to_send = []
        if len(self.list_of_new_album) == 0:
            print("No new album")
            return None
        for album in self.list_of_new_album:
            if album.name.lower() not in send_album:
                send_album.append(album.name.lower())
                to_send.append(album)
        for sender in senders:
            sender.send_notification(to_send, self.user)


def main():
    musicnotifier = MusicNotifier(40)
    musicnotifier.fetch(
        [
            "Neophron",
            "Femtogo",
            "Ptite Soeur",
            "Baby Hayabusa",
            "Luther",
            "Khali",
            "abel31",
            "Realo",
            "Wallace Cleaver",
        ],
        [SpotifyFetch(), SoundCloudFetch()],
    )
    musicnotifier.send([Notifier(), NotifierMail()])


if __name__ == "__main__":
    main()
