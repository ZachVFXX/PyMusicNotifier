from dataclasses import dataclass, field
import pendulum
from pendulum import DateTime
from typing import Protocol


@dataclass
class Artist:
    name: str
    image_url: str
    followers: int
    uri: str


@dataclass
class User:
    name: str


@dataclass(order=True)
class Album:
    name: str = field(compare=False)
    image_url: str = field(compare=False)
    uri: str = field(compare=False)
    type: str = field(compare=False)
    artist: list[str] = field(compare=False)
    link: str = field(compare=False)
    release_date: DateTime = field(default_factory=DateTime)

    def __post_init__(self) -> None:
        self.release_date = pendulum.from_format(self.release_date, "YYYY-MM-DD")

    def get_artists(self) -> str:
        return ", ".join(self.artist)


class Fetch(Protocol):
    def get_last_album_from_artist(artist: str) -> Album: ...

    def get_username() -> User: ...


class Sender(Protocol):
    def send_notification(albums: list[Album], user: User) -> None: ...
