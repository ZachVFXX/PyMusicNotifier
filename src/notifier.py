from notifypy import Notify
from img_util import url_to_img_path
from protocols import Album, User, Sender

from time_util import format_time_from_now


class Notifier(Sender):
    def __init__(self):
        self.notification = Notify(
            default_notification_application_name="pymusicnotifier"
        )

    def send_notification(self, album: Album, user: User) -> None:
        self.notification.title = f"{album.name} just released!"
        self.notification.icon = url_to_img_path(album)
        self.notification.message = f"{album.get_artists()} release a(n) {album.type} {format_time_from_now(album.release_date)}"
        self.notification.send()
