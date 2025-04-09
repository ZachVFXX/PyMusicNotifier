from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Artist:
    name: str
    image_url: str
    followers: int
    genres: list[str]
    uri: str


@dataclass(order=True)
class Album:
    name: str = field(compare=False)
    image_url: str = field(compare=False)
    uri: str = field(compare=False)
    type: str = field(compare=False)
    artist: list[str] = field(compare=False)
    release_date: datetime = field(default_factory=datetime)

    def __post_init__(self) -> None:
        self.release_date = datetime.strptime(self.release_date, "%Y-%m-%d")

    def get_artists(self) -> str:
        return ", ".join(self.artist)
