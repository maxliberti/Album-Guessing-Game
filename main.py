from dotenv import load_dotenv
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy_random import get_random


load_dotenv()
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret))
lastfm_api_key = os.getenv("LASTFM_CLIENT_ID")

def get_album_list_by_genre(genre):
    url = "http://ws.audioscrobbler.com/2.0/"
    parameters = {
        "method": "tag.gettopalbums",
        "tag": genre,
        "api_key": lastfm_api_key,
        "format": "json"
    }

    response = requests.get(url, params=parameters)
    jsondict = response.json()
    return jsondict['albums']['album']


hiphopalbumjson = get_album_list_by_genre("hip-hop")
hiphopalbumlist = []
for album in hiphopalbumjson:
    album_name = album['name']
    hiphopalbumlist.append(album_name)

for i in hiphopalbumlist:
    print(i)
