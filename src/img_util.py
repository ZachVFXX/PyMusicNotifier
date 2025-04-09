from pathlib import Path
from urllib.error import URLError
import requests
from protocols import Album


def url_to_img_path(album: Album) -> Path:
    path = Path(f"src/img/{album.get_artists()}{album.release_date.int_timestamp}.png")
    if path.exists():
        return path
    response = requests.get(album.image_url)
    if response.status_code != 200:
        raise URLError
    path.touch()
    with open(path, "wb") as f:
        f.seek(0)
        f.write(response.content)
    return path
