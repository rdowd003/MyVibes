from flask import Flask, render_template, request
import json
import requests
import socket
import time
import pickle
from datetime import datetime
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import spotipy
import os
from unidecode import unidecode
from codecs import encode,decode
import matplotlib




#Cluster Samples
with open('../data/big_popular3.pkl','rb') as f:
    clusters = pickle.load(f)

#Audio features matrix data with labels
with open('../data/AF_with_id.pkl','rb') as f2:
    AF_with_id = pickle.load(f2)

#Track info matrix with labels
with open('../data/track_info1.pkl','rb') as f3:
    track_info = pickle.load(f3)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/index.html', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/about.html', methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/products.html', methods=['GET','POST'])
def products():
    return render_template('products.html',data = clusters)

@app.route('/store.html', methods=['GET','POST'])
def store():
    return render_template('store.html')

@app.route('/recommendations', methods=['GET','POST'])
def song_recs():
    song_pref = int(request.form['cluster'])
    priority = str(request.form['feature'])
    level = str(request.form['level'])
    desired_pop = str(request.form['popular'])
    if song_pref == '':
        return 'You must select a cluster.'
    if priority == '':
        return 'You must select an audio feature.'
    else:
        AF_filtered = AF_with_id[AF_with_id['labels'] == song_pref-1]
        #AF_filtered.sort_values(by=['popularity'],ascending=False,inplace=True)
        avg_pop = AF_filtered['popularity'].mean()
        avg = AF_filtered[priority].mean()
        if level == 'high':
            AF_filtered_feature_choice = AF_filtered[AF_filtered[priority]>=avg]
        elif level == 'low':
            AF_filtered_feature_choice = AF_filtered[AF_filtered[priority]<avg]

        if desired_pop == 'high':
            AF_filtered_feature_choice = AF_filtered_feature_choice[AF_filtered_feature_choice['popularity']>=avg_pop]
        elif desired_pop == 'low':
            AF_filtered_feature_choice = AF_filtered_feature_choice[AF_filtered_feature_choice['popularity']<avg_pop]
        elif desired_pop == 'random':
            AF_filtered_feature_choice = AF_filtered_feature_choice
        rec_ids = []
        rec_titles = []
        rec_albums = []
        rec_artists = []
        rec_previews = []

        #Pick top 3 songs based on popularity
        for i in range(3):
            track_ids = np.random.choice(AF_filtered_feature_choice['id'],size=1,replace=False)[0]
            rec_ids.append(track_ids)
            title = list(track_info['name'][track_info['id']== track_ids])[0]
            print(title)
            title1 = title.encode('ascii','ignore').decode('unicode_escape')
            rec_titles.append(title1)
            artist = track_info['artist_name'][track_info['id']== track_ids].iloc[0][0]['name']
            rec_artists.append(artist)
            album = track_info['album'][track_info['id'] == track_ids].iloc[0]['name']
            rec_albums.append(album)
            preview = list(track_info['preview_url'][track_info['id'] == track_ids])[0]
            rec_previews.append(preview)


        rec_titles_clean = []
        rec_df = pd.DataFrame(rec_titles,columns=['Song_name'])
        rec_df['Album'] = rec_albums
        rec_df['Artists'] = rec_artists
        rec_df['Preview_link'] = rec_previews
        rec_df['Track_id'] = rec_ids

        return render_template('recommendations.html',data=rec_df)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True,threaded=True)
