import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the authentication flow
auth_manager = SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri='http://example.com',
    scope='playlist-modify-private',
    show_dialog=True,
    cache_path="token.txt"
)
access_token = auth_manager.get_access_token(as_dict=False)

# Create the Spotify instance
sp = spotipy.Spotify(auth=access_token)

user_id = sp.current_user()["id"]


user_input = input("Which year do you want to travel to Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names)

song_uris = []
year = user_input.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)