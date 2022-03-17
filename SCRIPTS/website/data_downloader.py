import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config
from typing import List, Any


class SpotifyData:
    """ Responible for downloading the data from Spotify. """
    def __init__(self, playlist_link: str):
        self.playlist_link = playlist_link.strip()
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def get_playlist_tracks(self) -> List:
        """ Get data for every track in playlist from Spotify API. """
        try:
            playlist_link = self.get_playlist_id(self.playlist_link)
            results = self.spotify.playlist_tracks(playlist_link)
            items = results['items']
            while results['next']:
                results = self.spotify.next(results)
                items.extend(results['items'])
            return [i['track'] for i in items]
        except spotipy.exceptions.SpotifyException:
            return []

    def get_tracks_features(self, playlist_tracks: List) -> List:
        """ Get features for every track in playlist_tracks - result of get_playlist_tracks method. """
        ids = [i['id'] for i in playlist_tracks]
        features = []
        while len(ids) > 0:
            str_ids = ",".join(ids[:100])
            features.extend(self.spotify.audio_features(str_ids))
            del ids[:100]
        return features
    
    def download_data(self):
        tracks = self.get_playlist_tracks()
        if tracks:
            features = self.get_tracks_features(tracks)
            return self.concat_data(tracks, features)
    
    @staticmethod
    def concat_data(tracks: List, features: List) -> List[dict[str, Any]]:
        data = []
        for track, feature in zip(tracks, features):
            t = {}
            t['artistName'] = track['artists'][0]['name']
            t['trackName'] = track['name']
            t['popularity'] = track['popularity']
            t['mode'] = feature['mode']
            t['acousticness'] = feature['acousticness']
            t['danceability'] = feature['danceability']
            t['energy'] = feature['energy']
            t['instrumentalness'] = feature['instrumentalness']
            t['liveness'] = feature['liveness']
            t['loudness'] = feature['loudness']
            t['speechiness'] = feature['speechiness']
            t['tempo'] = feature['tempo']
            t['valence'] = feature['valence']
            data.append(t)
        return data

    @staticmethod
    def get_playlist_id(playlist_link: str) -> str:
        start = playlist_link.find('playlist/')+len('playlist/')
        end = playlist_link.find('?')
        if end == -1:
            return playlist_link[start:]
        else:
            return playlist_link[start:end]



