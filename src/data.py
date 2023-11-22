import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()
global sp


class Spot:
    def __init__(self):
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")

        client_creds_mgr = SpotifyClientCredentials(client_id, client_secret)

        self.sp = spotipy.Spotify(client_credentials_manager=client_creds_mgr)

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


lk = input("Enter playlist: ")
stp = Spot()
ply = stp.get_playlist_contents(lk)

print(ply[0])
