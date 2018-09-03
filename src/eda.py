import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import pickle
from sklearn.metrics.pairwise import euclidean_distances
from song_clustering import run_optimal_kmeans,standardize,run_pca

def plot_vif(features):
    X = features.copy()
    X.drop(columns=['id','labels'],inplace=True)
    vif = pd.DataFrame()
    vif["VIF_Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["features"] = X.columns
    plt.bar(vif["features"],vif['VIF_Factor'])
    plt.ylabel('VIF')
    plt.title('Variable Inflation Factor Test on Full Popular Data Set')
    plt.xticks(rotation=85)
    plt.tight_layout()
    plt.show()

def plot_histogram_discrete(df,feature):
    plt.hist(df[feature])
    plt.show()

#plot_vif(AF_with_id)
#plot_histogram_discrete(AF_with_id,'time_signature')
#plot_histogram_discrete(AF_with_id,'mode')


#Audio features matrix data with labels
with open('../data/AF_with_id.pkl','rb') as f2:
    AF_with_id = pickle.load(f2)

#Track info matrix with labels
with open('../data/track_info.pkl','rb') as f3:
    track_info = pickle.load(f3)

#Calulate feature averages by cluster & check cluster similarities
AF = AF_with_id.copy()
AF = AF.drop(columns=['id'])
grouped = AF.groupby(['labels']).mean()
grouped_std = standardize(grouped)

similarity = euclidean_distances(grouped,grouped) #cluster 5 & 7 have largest ED

c1 = 5
c2 = 7
cluster1_means = grouped_std[c1,:]
cluster2_means = grouped_std[c2,:]

x = np.arange(len(cluster1_means))
X_cols = grouped.columns
w = 0.5
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
p1 = ax.bar(x,cluster1_means,w,color='red')
p2 = ax.bar(x+w,cluster2_means,w,color='blue')
ax.set_xlabel('Audio Features',fontsize=12)
ax.set_ylabel('Cluster Averages',fontsize=12)
ax.set_title('Standardized Feature Averages For Two Distant Clusters')
ax.legend((p1[0], p2[0]), ('Cluster 5', 'Cluster 7'))
plt.axhline(0, color='blue')
ax.set_xticks(x)
ax.set_xticklabels(X_cols)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#Plot min and max of each AF for all songs in top 20% of popularity
high_pop_thresh = (AF_with_id['popularity'].max())*0.8
high_pop = AF_with_id[AF_with_id['popularity']>high_pop_thresh]
#high_pop = AF_with_id.copy() - to plot for all songs
high_pop.drop(columns=['id','labels'],inplace=True)
std = standardize(high_pop)
std_df = pd.DataFrame(std,columns=high_pop.columns)
mins = np.array(std_df.min())
maxs = np.array(std_df.max())

x = np.arange(len(mins))
X_cols = high_pop.columns
w = 0.5
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
p1 = ax.bar(x,mins,w,color='red')
p2 = ax.bar(x,maxs,w,color='blue')
ax.set_xlabel('Audio Features',fontsize=12)
ax.set_ylabel('Minimum & Maximum',fontsize=12)
ax.set_title("Min & Max of Standardized Audio Features For Top 20% of Songs By Popularity")
ax.legend((p1[0], p2[0]), ('Min', 'Max'))
plt.axhline(0, color='blue')
ax.set_xticks(x)
ax.set_xticklabels(X_cols)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#
