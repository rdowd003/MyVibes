# Get data
import pandas as pd
import spotipy
import os

def get_playlist_tracks(username,playlist_id):
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

def get_popularity_and_ids(playlist):
    '''
    gets the popularity and id from a list of track objects, only if the track ID exists.
    playlist: a list of spotify track objects (dicts)
    returns:
        popularity: list of ints with the spotify popularity score
        ids: list of strings with the spotify URIs for each song
    '''
    popularity = []
    ids = []
    for i in range(len(playlist)):
        if playlist[i]['track']['id'] is not None:
            popularity.append(playlist[i]['track']['popularity'])
            ids.append(playlist[i]['track']['id'])
    return popularity, ids

def get_attributes(id_list):
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

def pop_ids_attr_to_data_frame(attribute_list, popularity_list):
    '''
    mushes together the popularity_list and the attribute_list and turns it into a dataframe.
    '''
    attr_df = pd.DataFrame(attribute_list)
    pop_df = pd.Series(popularity_list)
    attr_df["popularity"] = pop_df
    return attr_df

def scrape_playlist(playlist_info):

    my_playlist = get_playlist_tracks(playlist_info[0], playlist_info[1])

    #get popularity and song ids from from the track list
    pop, my_ids = get_popularity_and_ids(my_playlist)

    #get attributes from your id list
    my_attributes = get_attributes(my_ids)

    #mush everything together
    dataframe = pop_ids_attr_to_data_frame(my_attributes, pop)

    return dataframe

#Connect to Spotify API
sp = spotipy.Spotify()
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY'), client_secret=os.getenv('SPOTIFY_SECRET_KEY'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

playlists_to_scrape = [("whitneypenn", "spotify:user:whitneypenn:playlist:44sRyzuMuFwNUGq6otEvGG")]

a = scrape_playlist(playlists_to_scrape[0])
if len(playlists_to_scrape) > 0:
    for i in range(1, len(playlists_to_scrape)):
        a = a.append(scrape_playlist(playlists_to_scrape[i]))


a.to_csv('~/Galvanize/analytics-capstone/data/unseen_data.csv')
