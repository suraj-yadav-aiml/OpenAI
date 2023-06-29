import openai
import spotipy
from dotenv import dotenv_values

from pprint import pprint

config_openai = dotenv_values("../../../.env")
config_spotify = dotenv_values("./.spotify_env")

sp = spotipy.Spotify(
    auth_manager = spotipy.SpotifyOAuth(
        client_id = config_spotify["SPOTIFY_CLIENT_ID"],
        client_secret = config_spotify["SPOTIFY_CLIENT_SECRET"],
        redirect_uri = "https://localhost:9999",
        scope = "playlist-modify-private"
    )
)

current_user = sp.current_user()
assert current_user is not None 

search_result = sp.search(q="Din Shagna Da", type='track', limit=10)

created_playlist = sp.user_playlist_create(
    current_user["id"],
    public=False,
    name = "Test Run ... "
)

tracks = [search_result['tracks']['items'][0]["id"]]
sp.user_playlist_add_tracks(
    current_user["id"],
    created_playlist["id"],
    tracks
)




