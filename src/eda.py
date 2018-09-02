import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('../data/spotify_data.csv')


with open('../data/AF_with_id.pkl','rb') as f2:
    AF_with_id = pickle.load(f2)

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

plot_vif(AF_with_id)

def plot_histogram_discrete(df,feature):
    plt.hist(df[feature])
    plt.show()

plot_histogram_discrete(AF_with_id,'time_signature')
plot_histogram_discrete(AF_with_id,'mode')

#subplots to generate:
#Average 
