import openai
import spotipy
import json
from dotenv import dotenv_values
import argparse


config_openai = dotenv_values("../../../.env")
config_spotify = dotenv_values("./.spotify_env")

parser = argparse.ArgumentParser(description="Simple command line Spotify Playlist creater.")
parser.add_argument("-p", type=str, help="The prompt to describe the playlist")
parser.add_argument("-n", type=int, help="Number of songs in Playlist", default=8)

args = parser.parse_args()

def get_playlist(text_prompt, count=8):
    
    example_json = """
    [
    {"song": "Rang Barse", "artist": "DJ Shadow Dubai"},
    {"song": "Ang Se Ang Lagana", "artist": "DJ Lloyd"},
    {"song": "Holi Khele Raghuveera", "artist": "DJ NYK"},
    {"song": "Balam Pichkari", "artist": "DJ Saurabh"},
    {"song": "Do Me a Favor Let's Play Holi", "artist": "DJ Aqeel"},
    {"song": "Badri Ki Dulhania (Title Track)", "artist": "DJ Chetas"},
    {"song": "Go Pagal", "artist": "DJ Shilpi Sharma"},
    {"song": "Aaj Na Chhodenge", "artist": "DJ Ishwar"},
    {"song": "Hori Khele Raghuveera (Remix)", "artist": "DJ Dalal London"}
    ]
    """
    messages = [
        {"role":"system", "content":"""
        You are helpful playlist generating assistant.
        You should generate a list of songs and thier artist according to text prompt.
        You should return a JSON array, where each element follows this format: 
        {"song":<song_title>,"artist":<artist_name>}
        """},
        {'role':'user', 'content':"Generate a playlist of 9 songs based on this prompt : Holi songs for 2023 with DJ style"},
        {'role':'assistant', 'content':example_json},
        {'role':'user', 'content':f"Generate a playlist of {count} songs based on this prompt : {text_prompt}"}
    ]

    response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages,
                max_tokens = 400
    )

    return json.loads(response['choices'][0]['message']['content'])


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

genrated_song_list = get_playlist(args.p,args.n)

track_ids = []
for item in genrated_song_list:
    song, artist = item['song'], item['artist']
    query = f"{song} {artist}"
    search_result = sp.search(q=query, type='track', limit=10)
    track_ids.append(search_result['tracks']['items'][0]["id"])

created_playlist = sp.user_playlist_create(
    current_user["id"],
    public=False,
    name = args.p
)

sp.user_playlist_add_tracks(
    current_user["id"],
    created_playlist["id"],
    track_ids
)

print("Playlist created !!!")


