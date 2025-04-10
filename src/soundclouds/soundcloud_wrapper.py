from soundcloud import SoundCloud
import requests_cache
from protocols import Album, User

requests_cache.install_cache("src/soundclouds/soundcloud_cache", expire_after=3600)


class SoundCloudFetch:
    def __init__(self) -> None:
        client_id: str = SoundCloud.generate_client_id()
        self.api = SoundCloud(
            client_id=client_id,
        )
        assert self.api.is_client_id_valid()

    def get_user_id_from_artist_name(self, artist_name: str) -> str | None:
        artist = self.api.search_users(artist_name).__next__()
        return artist.id

    def get_artist_discography(self, artist_user_id: str) -> list[Album]:
        albums = list(self.api.get_user_tracks(artist_user_id))
        return [
            Album(
                album.title,
                album.artwork_url,
                album.uri,
                "track",
                [album.user.username],
                album.permalink_url,
                album.created_at.strftime("%Y-%m-%d"),
            )
            for album in albums
        ]

    def get_last_album_from_artist(self, artist_name: str) -> Album | None:
        id = self.get_user_id_from_artist_name(artist_name)
        if id:
            disco = self.get_artist_discography(id)
            if disco:
                return max(disco)
        return None

    def get_username(self) -> str:
        return User(name="Zach")
