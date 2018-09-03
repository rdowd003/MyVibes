#Clustering

import pandas as pd
import numpy as np
import spotipy
import os
from pull_data import CleanData,SpotifyPlaylist
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from pyspark.mllib.clustering import KMeans


def standardize(raw_df):
    scaler = StandardScaler()
    feats_std = scaler.fit_transform(raw_df)
    return feats_std

def run_pca(standardized_features):
    pca = PCA()
    X_reduced = pca.fit_transform(standardized_features)
    return (pca,X_reduced)

def scree_plot(ax, pca_object, n_components_to_plot,
title='Explained Variance for n=15 Principle Components'):
    num_components = pca_object.n_components_
    ind = np.arange(num_components)
    print(ind)
    vals = pca_object.explained_variance_ratio_
    print(vals)
    ax.plot(ind, vals, color='blue')
    ax.scatter(ind, vals, color='blue', s=50)

    for i in range(num_components):
            ax.annotate(r"{:2.2f}%".format(vals[i]),
            (ind[i]+0.2, vals[i]+0.005),
            va="bottom",
            ha="center",fontsize=12)

    ax.set_ylim(0, max(vals) + 0.05)
    ax.set_xlim(0 - 0.45, n_components_to_plot + 0.45)
    ax.set_xlabel("Principal Component", fontsize=10)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)
    if title is not None:
        ax.set_title(title, fontsize=12)



def elbow_plot(ax,standardized_X,min,max,step=1):
    distortions = []
    K = range(min,max,step)
    for k in K:
        kmeanModel = MiniBatchKMeans(n_clusters=k,init='k-means++',batch_size=100)
        kmeanModel.fit(standardized_X)
        distortions.append(sum(np.min(cdist(standardized_X, kmeanModel.cluster_centers_,
         'euclidean'), axis=1)) / standardized_X.shape[0])
    # Plot the elbow
    print(distortions)
    print(K)
    ax.plot(K, distortions, 'bx-')
    ax.set_xlabel('k',fontsize=10)
    ax.set_ylabel('Distortion')
    ax.set_title('Optimal k for Audio Features (w/o PCA)',fontsize=12)



def run_optimal_kmeans(X,k):
    n_clusters = k
    kmeans = MiniBatchKMeans(n_clusters=k,init='k-means++',batch_size=100)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_
    labels = pd.Series(labels)
    labeled_X = pd.DataFrame(X)
    labeled_X['labels'] = labels
    return (labeled_X,labels,centroids)

'''
TEST data
#Get data
df = CleanData('../data/spotify_data.csv')
df.make_df()
df.add_local_id() #using this to make my own track id, for now (not used  yet)
AF,track_info = df.features()

'''

sp = spotipy.Spotify()
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY'), client_secret=os.getenv('SPOTIFY_SECRET_KEY'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

playlist = SpotifyPlaylist()
df_unclean = playlist.get_data()
df_clean = CleanData(df_unclean)
AF,track_info = df_clean.features()
popularity = AF.pop('popularity')
ids = AF.drop('id')


#Standardize and Reduce (with PCA) raw audio features

AF_std = standardize(AF)
pca,AF_std_reduced = run_pca(AF_std)


#Scree and elbow plot for optimal PC's and optimal number (k) clusters

fig,(ax1,ax2) = plt.subplots(2,1,sharey=False,figsize=(10,6))

n_comps = AF_std_reduced.shape[1]
scree_plot(ax1,pca,n_comps)
elbow_plot(ax2,AF_std,1,50,2)
plt.tight_layout()
plt.savefig('../data/elbow_scree.png')



# Single K-Means with optimal #PC's and optimal K
n_clusters = 10
x_df_label,labels,centers = run_optimal_kmeans(AF_std_reduced,n_clusters)

AF_STD_reduced['labels'] = labels

#Plot clusters
fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(AF_STD_reduced[:,0], AF_STD_reduced[:, 1], c=labels, s=50, cmap='viridis')
ax.set_title('Librosa K-Means Clustering (k=5, n_pc = 6)')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
plt.colorbar(scatter)
plt.show()
