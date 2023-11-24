import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import pandas as pd
from collections import defaultdict


number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

load_dotenv()


class Spot:
    def __init__(self):
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")

        client_creds_mgr = SpotifyClientCredentials(client_id, client_secret)

        self.sp = spotipy.Spotify(client_credentials_manager=client_creds_mgr)

    def find_song(self, name, year):
        song_data = defaultdict()
        results = self.sp.search(q= 'track: {}'.format(name), limit=1)
        print(results)
        if results['tracks']['items'] == []:
            return None

        results = results['tracks']['items'][0]
        track_id = results['id']
        audio_features = self.sp.audio_features(track_id)[0]

        song_data['name'] = [name]
        song_data['year'] = [year]
        song_data['explicit'] = [int(results['explicit'])]
        song_data['duration_ms'] = [results['duration_ms']]
        song_data['popularity'] = [results['popularity']]

        for key, value in audio_features.items():
            song_data[key] = value

        return pd.DataFrame(song_data)


    def get_playlist_contents(self, link):
        playlist_URI = link.split("/")[-1].split("?")[0]
        tracks = []
        for track in self.sp.playlist_tracks(playlist_URI)["items"]:
            # print(track["track"])
            trck = {}
            # trck["uri"] = track["track"]["uri"]
            trck["track_name"] = track["track"]["name"]
            artists = track["track"]["artists"]
            trck["artist_name"] = artists[0]["name"]
            genre = self.sp.artist(artists[0]["uri"])["genres"]
            trck["genre"] = genre
            # print("--->", trck["artist"])
            trck["album"] = track["track"]["album"]["name"]
            trck["popularity"] = track["track"]["popularity"]
            feats = self.sp.audio_features(track["track"]["uri"])[0]
            for x, y in feats.items():
                trck[x] = y
            tracks.append(trck)
        return tracks

