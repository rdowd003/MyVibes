#Data cleaning
import pandas as pd
import numpy as np
import spotipy
import os

class SpotifyPlaylist:
    def __init__(self):
        pass
    def get_playlist_tracks(self,username,playlist_id):
        '''pulls down tracks from the spotify API
        username: str, username of the account that made the playlistself.
        playlist_id: str, the URI of the spotify playlist
        returns: a list of spotify track objects (dicts) for every song in the playlist.
        '''
        results = sp.user_playlist_tracks(username,playlist_id)
        tracks = results['items']
        #this loops through the track pages to make sure you get every song
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks

    def get_popularity_and_ids(self,playlist):
        '''
        gets the popularity and id from a list of track objects, only if the track ID exists.
        playlist: a list of spotify track objects (dicts)
        returns:
            popularity: list of ints with the spotify popularity score
            ids: list of strings with the spotify URIs for each song
        '''
        popularity = []
        ids = []
        artists = []
        albums = []
        names = []
        previews = []
        for i in range(len(playlist)):
            if playlist[i]['track']['id'] is not None:
                popularity.append(playlist[i]['track']['popularity'])
                ids.append(playlist[i]['track']['id'])
                artists.append(playlist[i]['track']['artists'])
                albums.append(playlist[i]['track']['album'])
                names.append(playlist[i]['track']['name'])
                previews.append(playlist[i]['track']['preview_url'])
        return ids, popularity, artists, names, albums, previews

    def get_attributes(self,id_list):
        '''
        gets the song attributes from each song in your id_list
        id list: a list of strings that are spotify URIs
        returns: a list of dicts containing the song attributes for each song.
        '''
        results = []
        attributes_by_song = []
        slices = [id_list[i:i+50] for i in range(0, len(id_list), 50)]
        for i in slices:
            results.append(sp.audio_features(i))
        for i in results:
            for j in i:
                attributes_by_song.append(j)
        return attributes_by_song

    def pop_ids_attr_to_data_frame(self,attribute_list, popularity_list):
        '''
        mushes together the popularity_list and the attribute_list and turns it into a dataframe.
        '''
        attr_df = pd.DataFrame(attribute_list)
        pop_df = pd.Series(popularity_list)
        attr_df["popularity"] = pop_df
        return attr_df

    def scrape_playlist(self,playlist_info):

        my_playlist = self.get_playlist_tracks(playlist_info[0], playlist_info[1])

        #get popularity and song ids from from the track list
        my_ids, pop, artists, names, albums, previews = self.get_popularity_and_ids(my_playlist)

        #get attributes from your id list
        my_attributes = self.get_attributes(my_ids)

        df = pd.DataFrame(my_attributes)

        feat_names = ['popularity','id','artists','name','album','preview_url']
        feat_lists = [pop, my_ids, artists, names, albums, previews]
        features_to_merge = zip(feat_names,feat_lists)

        for i,k in features_to_merge:
            df[i] = pd.Series(k)


        #merge everything together
        #dataframe = self.pop_ids_attr_to_data_frame(my_attributes, pop)

        return df

    def get_data(self):
        playlists_to_scrape = [("12160726861", "spotify:user:12160726861:playlist:6yPiKpy7evrwvZodByKvM9")]

        a = self.scrape_playlist(playlists_to_scrape[0])
        if len(playlists_to_scrape) > 0:
            for i in range(1, len(playlists_to_scrape)):
                a = a.append(self.scrape_playlist(playlists_to_scrape[i]))

        return a


'''
Clean Spotify playlist and split into appropriate data frames
'''

class CleanData:
    def __init__(self,pulled_df,filepath=None):
        self.pulled_df = pulled_df
        self.filepath = filepath
        self.df = pd.DataFrame()
        self.track_info_df = pd.DataFrame()
        self.audio_feature_df = pd.DataFrame()

    def make_df(self):
        if not filepath:
            self.df = self.pulled_df
        else:
            self.df = pd.read_csv(self.filepath)

    def add_local_id(self):
        self.df['local_id']= self.pulled_df.index

    def features(self):
        self.audio_feature_df = self.pulled_df[['id',
                            'acousticness',
                            'danceability',
                            'duration_ms',
                            'energy',
                            'instrumentalness',
                            'key',
                            'liveness',
                            'loudness',
                            'mode',
                            'speechiness',
                            'tempo',
                            'time_signature',
                            'valence',
                            'popularity']]

        self.track_info_df = self.pulled_df[['analysis_url',
                                        'id',
                                        'artists',
                                        'album',
                                        'name',
                                        'preview_url',
                                        'track_href',
                                        'type',
                                        'uri']]

        artists_names = self.track_info_df['artists'].copy()
        self.track_info_df['artist_name'] = artists_names.values
        self.track_info_df.drop(columns={'artists'},inplace=True)
        return (self.audio_feature_df,self.track_info_df)



'''
TEST with saved data (2500 tracks)

df = CleanData('../data/spotify_data.csv')
df.make_df()
df.add_local_id()
audio_feats = df.features()[0]
track_info = df.features()[1]
'''

sp = spotipy.Spotify()
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY'), client_secret=os.getenv('SPOTIFY_SECRET_KEY'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

'''
playlist = SpotifyPlaylist()
df_unclean = playlist.get_data()
df_clean = CleanData(df_unclean)
df_clean.add_local_id()
audio_feats,track_info = df_clean.features()




("captain25", "spotify:user:captain25:playlist:45W54xcJIsBnLXpdnsdVRL")
spotify:user:12160726861:playlist:6yPiKpy7evrwvZodByKvM9
'''

#
