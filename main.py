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

album_id_list = []

load_dotenv()

with open("albumlist.txt", 'r') as album_id_text:
    album_id_list = [line.strip() for line in album_id_text]

def print_album_info():
    for id in album_id_list:
        album_details = spotify_client.album(id)
        tracklist_details = spotify_client.album_tracks(id)

        # print album cover url
        album_cover_url = album_details['images'][0]['url']
        print(f"Album cover url: {album_cover_url}")

        # print album name
        album_name = album_details['name']
        print(f"Album: {album_name}")

        # print artist names
        artist_name = album_details['artists']
        for artist in artist_name:
            print(f"Artist: {artist['name']}")

        # print tracklist
        tracklist = tracklist_details['items']
        for track in tracklist:
            print(f"Track {track['track_number']}: {track['name']}")

        # print total tracks
        total_tracks = tracklist_details['total']
        print(f"Total tracks: {total_tracks}")

        # print release date
        release_date = album_details['release_date']
        print(f"Release date: {release_date}")


print_album_info()


