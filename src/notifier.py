from notifypy import Notify
from protocols import Album


class Notifier:
    def __init__(self):
        self.notification = Notify(
            default_notification_application_name="pymusicnotifier"
        )

    def send_notification(self, album: Album):
        self.notification.title = f"{album.name} just released!"
        self.notification.message = f"Artist: {', '.join(album.artist)}\nReleased: {album.release_date.strftime('%d/%m/%Y')}"
        self.notification.send()
