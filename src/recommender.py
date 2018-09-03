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
popularity = AF.pop('popularity')


#Standardize and Reduce (with PCA) raw audio features
AF_std = standardize(AF)
AF_std_reduced = run_pca(AF_std)[1]

#Cluster songs; returns features data frame with labels attached
n_clusters = 10
labeled_features,labels,centers = run_optimal_kmeans(AF_std_reduced,n_clusters)

#PICKLE THIS WHEN YOU'RE READY WITH FINAL PLAYLIST DATASET (add more in pull_data)
track_info['labels'] = labels
AF_with_id['labels'] = labels

#AF_with_id.to_pickle('/data/AF_with_id1.pkl')
#track_info.to_pickle('/data/track_info1.pkl')

'''
Creating Cluster Samples for Step 1

#!!!! Cluster choice Dataframe has been pickled - do not need to uncomment unless to change songs !!!!

#1) Choose k (number of clusters = 10) random tracks for choice

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
