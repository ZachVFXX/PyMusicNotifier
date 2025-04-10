from notifypy import Notify
from img_util import url_to_img_path
from protocols import Album, User, Sender

from time_util import format_time_from_now


class Notifier(Sender):
    def __init__(self):
        self.notification = Notify(
            default_notification_application_name="pymusicnotifier"
        )

    def send_notification(self, albums: list[Album], user: User) -> None:
        list_title = []
        list_content = []
        for album in albums:
            list_title.append(album.name)
            list_content.append(
                f"{album.get_artists()} release a(n) {album.type} {format_time_from_now(album.release_date)}"
            )
        self.notification.title = f"{', '.join(list_title)} just released!"
        self.notification.icon = url_to_img_path(albums[0])
        self.notification.message = f"{', '.join(list_content)}"
        self.notification.send()

    def __repr__(self): ...
