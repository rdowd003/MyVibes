# MyVibes: A Musical Recommender
Galvanize 2018 DSI: Final Capstone

[Check it out here!](http://ec2-52-20-14-87.compute-1.amazonaws.com:8080/index.html)

____
### What is MyVibes?

MyVibes is a song-recommender that is driven by users' connection
to the deeper elements of music. The recommender system has been deployed as a
web-application (mobile friendly) through the implementation of Flask and AWS
instances. While there are indeed many recommenders that already exist, the
unique architecture of this system allows for fast, user-preference driven recommendations
that will undoubtedly change things up.

____
### How Is It Built?

The recommender system is built around a 10,000 track playlist, and focuses on 14 audio
features delivered through the Spotify API.

The 14 audio features are derivatives of the raw audio files, and are proprietary
to Spotify/Echonest. For each feature, there is a wide range of values within
the 10,000 track playlist (figure 1). The features include:
acoustiness, danceability, duration, energy, instrumentalness, musical key,
loudness, mode (major/minor), speechiness, tempo, time-signature and
valence ("happiness").

Figure 1: Feature Value Ranges

![featurerange](https://github.com/rdowd003/Capstone-3/blob/master/images/all_songs_range.png)

The driving force behind this unique recommender system is Kmeans clustering, that
ultimately groups each of the 10,000 tracks into 1 of 10 "vibes". The idea here,
is that tracks are grouped by similarities in the more complex elements of
music, rather than objective organizers like *artist*, *track name*, *genre*, etc.

This vibe clustering accomplishes two things:

1. The recommendation process is faster, as recommendations will be pulled from a
cluster (vibe) of songs that the user has already indicated a preference for,
rather than iteratively going song by song to make new offerings

2. The recommendations are driven by subjective-cognitive experiences, making
them more unique and personalized.


To reduce collinearity, principle component analysis was conducted, reducing the
number of features used in clustering, down to an optimal 10 (figure 2, top).
After just 2 principle components, roughly 34% of the data's variation can be
explained (figure 3)Additionally,an elbow-plot analysis was conducted to determine
that 10 was also the optimal number of clusters (figure 2, bottom). This number
was derived from two factors. The first, being minimization of cluster distortion,
standard practice associated with Kmeans clustering. The second factor, was a
practical limitation, in the time it should take users to utilize the recommender.

Figure 2: PCA scree plot and Elbow plot

![fig2](https://github.com/rdowd003/Capstone-3/blob/master/images/elbow_scree.png)

Figure 3.

![fig3](https://github.com/rdowd003/Capstone-3/blob/master/images/cluster_plot_final.png)

On to using the recommender!
____
### How do I get recommendations?

***To test it yourself visit:***

ec2-52-20-14-87.compute-1.amazonaws.com:8080

Or use the following QR code!
![QRcode](https://github.com/rdowd003/Capstone-3/blob/master/images/frame.png)


#### The recommender proceeds as follows:

<h2> STEP 1: Preview clusters</h2>

A user will preview a song-selection from each of the 10 vibes to find the best fit

![Step1](https://github.com/rdowd003/Capstone-3/blob/master/images/Screen%20Shot%202018-09-06%20at%201.22.13%20PM%20copy.png)

<h2> STEP 2: Select best cluster and feature preferences</h2>

After previewing vibes, the user will select a few preference to tailor their recommendations

![Step2](https://github.com/rdowd003/Capstone-3/blob/master/images/Screen%20Shot%202018-09-06%20at%201.49.37%20PM.png)

<h2> Get Recommendations and repeat! </h2>

The user can listen to their recommendations and then get new ones!

![Recommendations!](https://github.com/rdowd003/Capstone-3/blob/master/images/Screen%20Shot%202018-09-06%20at%201.47.03%20PM.png)
