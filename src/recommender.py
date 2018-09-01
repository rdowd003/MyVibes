import pandas as pd
import numpy as np
from pull_data import CleanData,SpotifyPlaylist
from song_clustering import run_optimal_kmeans,standardize,run_pca
import spotipy
import os


#Get data

sp = spotipy.Spotify()
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY'), client_secret=os.getenv('SPOTIFY_SECRET_KEY'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

playlist = SpotifyPlaylist()
df_unclean = playlist.get_data()
df_clean = CleanData(df_unclean)
AF_with_id,track_info = df_clean.features()

#copy AF and drop id, need id's later for label filtering
AF = AF_with_id.copy()
ids = AF.pop('id')


#Standardize and Reduce (with PCA) raw audio features
AF_std = standardize(AF)
AF_std_reduced = run_pca(AF_std)[1]

#Cluster songs; returns features data frame with labels attached
n_clusters = 10
labeled_features,labels,centers = run_optimal_kmeans(AF_std_reduced,n_clusters)

#PICKLE THIS ONE YOU'RE READY WITH FINAL PLAYLIST DATASET (add more in pull_data)
track_info['labels'] = labels
AF_with_id['labels'] = labels


#RECOMMENDING!


#!!!! Cluster choice Dataframe has been pickled - do not need to uncomment unless to change songs !!!!

#1) Choose k (number of clusters = 28) random tracks for choice

cluster_ids = []
titles = []
artists_list = []
urls = []
cluster_labels = []

temp = track_info.copy()

#go through all possible labels, select a random song, one from each cluster
for i in set(labels):
    cluster_labels.append(str(i+1))
    new_temp = temp[temp['labels']==i]
    c = np.random.choice(new_temp['id'],size=1)[0]

    while list(track_info['preview_url'][track_info['id']== c])[0] is None:
        c = np.random.choice(new_temp['id'],size=1)[0]
    cluster_ids.append(c)
    title = list(track_info['name'][track_info['id']== c])[0]
    titles.append(title)
    artist = track_info['artist_name'][track_info['id']== c].iloc[0][0]['name']
    artists_list.append(artist)
    url = list(track_info['preview_url'][track_info['id']==c])[0]
    urls.append(url)


df = pd.DataFrame(cluster_labels,columns=['cluster_labels'])
df['Track_id'] = cluster_ids
df['titles'] = titles
df['artists_list'] = artists_list
df['previews'] = urls

df.to_pickle('../data/big_popular3.pkl')

'''

#ALL OF THIS HA TO GO IN App.py ONCE I FIGURE OUT HOW TO GET RESPONSES TO
#NEXT PAGE

# SO I WILL NEED TO PICKLE AF_with_id, track_info, BOTH WITH LABELS

#User chooses cluster
#song_pref = input('Which song (1-10) did you enjoy the most? ') from flask
song_pref = 4

#Sort full song-matrix by label to isoalte songs in chosen cluster
AF_filtered = AF_with_id[AF_with_id['labels'] == song_pref]
AF_filtered.sort_values(by=['popularity'],ascending=False,inplace=True)

#Chosen feature to prioritize - example = tempo
priority = 'tempo'
avg = AF_filtered[priority].mean()
AF_filtered_feature_choice = AF_filtered[AF_filtered[priority]>avg]

rec_ids = []
rec_titles = []
rec_albums = []
rec_artists = []
rec_previews = []

#Pick top 3 songs based on popularity

x = AF_filtered_feature_choice[0:3]
for index, row in x.iterrows():
    track_ids = row['id']
    rec_ids.append(track_ids)
    title = list(track_info['name'][track_info['id']== track_ids])[0]
    rec_titles.append(title)
    artist = track_info['artist_name'][track_info['id']== track_ids].iloc[0][0]['name']
    rec_artists.append(artist)
    album = track_info['album'][track_info['id'] == track_ids].iloc[0]['name']
    rec_albums.append(album)
    preview = list(track_info['preview_url'][track_info['id'] == track_ids])[0]
    rec_previews.append(preview)

rec_df = pd.DataFrame(rec_titles,columns=['Song name'])
rec_df['Album'] = rec_albums
rec_df['Artists'] = rec_artists
rec_df['Preview link'] = rec_previews
rec_df['Track_id'] = rec_ids

print(rec_df.head())

'''
