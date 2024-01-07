import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret))

album_id_list = []

with open("albumlist.txt", 'r') as album_id_text:
    album_id_list = [line.strip() for line in album_id_text]

def create_album_info_dict(album_id_list):
    album_info = {}
    for id in album_id_list:
        album_details = spotify_client.album(id)
        tracklist_details = spotify_client.album_tracks(id)

        # album detail variable assignments
        album_cover_url = album_details['images'][0]['url']
        album_name = album_details['name']
        artist_names = [artist['name'] for artist in album_details['artists']]
        tracklist = [track['name'] for track in tracklist_details['items']]
        total_tracks = tracklist_details['total']
        release_date = album_details['release_date']

        album_info[id] = {
            "album_cover_url": album_cover_url,
            "album_name": album_name,
            "artist_names": artist_names,
            "tracklist": tracklist,
            "total_tracks": total_tracks,
            "release_date": release_date
        }

    return album_info

album_info_dict = create_album_info_dict(album_id_list)

# debug function
def print_filtered_list():
    for id, info in album_info_dict.items():
        print(f"Album ID: {id}")
        for key, value in info.items():
            if key == 'artist_name':
                print(f" {key}:")
                for artist in value:
                    print(f"    - {artist}")
            elif key == 'tracklist':
                print(f" {key}:")
                for track in value:
                    print(f"    - {track}")
            else:
                print(f" {key}: {value}")
        print()

print_filtered_list()