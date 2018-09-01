from flask import Flask, render_template, request
import json
import requests
import socket
import time
import pickle
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import spotipy
import os



#from pull_data import SpotifyPlaylist,CleanData
with open('../data/big_popular2.pkl','rb') as f:
    clusters = pickle.load(f)

with open('../data/AF_with_id.pkl','rb') as f2:
    recs = pickle.load(f2)


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

'''
@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    color_lst = None
    if request.form.get('green'):
        color_lst = ['green']
    if request.form.get('blue'):
        color_lst = ['green','blue']
    if request.form.get('black'):
        color_lst = ['green','blue','black']
    if request.form.get('bb'):
        color_lst = ['green','blue','black','bb']
    # CHECKBOX FUNCTIONALITY!!!
    resort = request.form['resort']
    if resort == '':
        return 'You must select a trail from your favorite resort.'
    trail = request.form['trail']
    if trail != '':
        index = int(trail)
        dest_resort = request.form['dest_resort']
        num_recs = int(request.form['num_recs'])
        rec_df = cos_sim_recs(index,num_recs,dest_resort,color_lst)
        rec_df = clean_df_for_recs(rec_df)
        if dest_resort == '':
            resort_links = links[resort]
        else:
            resort_links = links[dest_resort]
        return render_template('recommendations.html',rec_df=rec_df,resort_links=resort_links)
    return 'You must select a trail.'

'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True,threaded=True)
