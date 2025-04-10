from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests_cache
from protocols import Album, User

# Set up requests cache
requests_cache.install_cache("src/spotify/spotify_cache", expire_after=3600)


load_dotenv()


class SpotifyFetch:
    def __init__(self):
        self.api = spotipy.Spotify(auth_manager=SpotifyOAuth())

    def get_uri_from_artist_name(self, artist_name: str) -> str | None:
        results = self.api.search(q="artist:" + artist_name, type="artist")
        items = results["artists"]["items"]
        if len(items) > 0:
            artist = items[0]
            return artist.get("uri", None)
        else:
            return None

    def get_artist_discography(self, artist_uri: str) -> list[Album]:
        results: dict = self.api.artist_albums(artist_uri, limit=50)
        results: list[dict] = results.get("items")
        albums = []
        for album in results:
            artist_data = album.get("artists", None)
            if artist_data:
                artists = [
                    artist.get("name", "Error fetching name") for artist in artist_data
                ]
            else:
                artists = "Unknown artist"
            name = album.get("name", "Unknown name")
            image_url = album["images"][0]["url"]
            uri = album.get("uri", "Unknown uri")
            type = album.get("type", "Unknown album")
            release_date = album.get("release_date", "Unknown release date")

            external_urls = album.get("external_urls", None)
            if external_urls:
                external_urls = external_urls.get("spotify", None)
            albums.append(
                Album(
                    name=name,
                    image_url=image_url,
                    uri=uri,
                    type=type,
                    artist=artists,
                    release_date=release_date,
                    link=external_urls,
                )
            )
        return albums

    def get_last_album_from_artist(self, artist_name: str) -> Album | None:
        uri = self.get_uri_from_artist_name(artist_name)
        if uri:
            disco = self.get_artist_discography(uri)
            album = max(disco)
            return album
        return None

    def get_username(self) -> User:
        user: dict = self.api.current_user()
        username = user.get("display_name", "Unknown username")
        return User(name=username)

    def __repr__(self) -> str:
        return f"Spotify {self.get_username().name}"
