from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests_cache
from protocols import Album

# Set up requests cache
requests_cache.install_cache("src/spotify/spotify_cache", expire_after=180)


load_dotenv()


class SpotifyFetch:
    def __init__(self):
        self.api = spotipy.Spotify(auth_manager=SpotifyOAuth())
        self.artists_ids: list[str]

    def get_uri_from_artist_name(self, artist_name: str) -> str | None:
        results = self.api.search(q="artist:" + artist_name, type="artist")
        items = results["artists"]["items"]
        if len(items) > 0:
            artist = items[0]
            return artist["uri"]
        else:
            return None

    def get_artist_discography(self, artist_uri: str) -> list[Album]:
        results = self.api.artist_albums(artist_uri, limit=50)
        results = results["items"]
        albums = []
        for album in results:
            artists = [artist["name"] for artist in album["artists"]]
            name = album["name"]
            image_url = album["images"][0]["url"]
            uri = album["uri"]
            type = album["type"]
            release_date = album["release_date"]
            albums.append(
                Album(
                    name=name,
                    image_url=image_url,
                    uri=uri,
                    type=type,
                    artist=artists,
                    release_date=release_date,
                )
            )
        return albums
