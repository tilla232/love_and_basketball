import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score

from functions import cluster_and_plot

stats = pd.read_csv('../data/fornowstats.csv')
stats.set_index('player',inplace=True)
for_cluster = ['G','MP','WS','GS','MP.1','PER','3PAr','FTr','ORB%','DRB%','TRB%','AST%','STL%','BLK%','TOV%','USG%','ORtg','DRtg','OWS','DWS','WS/48','OBPM','DBPM','BPM','VORP','paint_rebounding','3catch_and_shoot','pullupshoot']

X = stats[for_cluster]
cluster_list = range(4,15)

def k_mean_score(n,scoring='rss'):
    km = KMeans(n_clusters=n, init ='k-means++', algorithm='elkan')
    km.fit(X)
    rss = -km.score(X)
    silhouette = silhouette_score(X,km.labels_)
    if scoring == 'rss':
        return rss
    else:
        return silhouette
# scores = [k_mean_score(k) for k in cluster_list]
# for k,score in enumerate(scores):
#     print "{}    |    {}".format(k+1,score)

# In [1]: run k_means_exploratory.py
# 1    |    8325322.6551
# 2    |    5413418.04159
# 3    |    4040109.70763
# 4    |    2986544.70563
# 5    |    2363667.84384
# 6    |    1893952.68636
# 7    |    1619210.52643
# 8    |    1374222.40621
# 9    |    1180948.31356
# 10    |    991495.772153
# 11    |    879363.16328

# WOW those are high!  We expect some difficulty interpreting this number given a large feature-space, but these numbers are too big to ignore.  Let's trim the feature-space a bit, trying to account for feature collinearity.  I'm also going to normalize the data, another step which should help with those rss figures

for_cluster = ['G','MP','GS','3PAr','FTr','ORB%','DRB%','AST%','STL%','BLK%','TOV%','USG%','OWS','DWS','WS/48','OBPM','DBPM','VORP']
X = normalize(stats[for_cluster])

# scores = [k_mean_score(k) for k in cluster_list]
# for k,score in enumerate(scores):
#     print "{}    |    {}".format(k+2,score)

# 1    |    6.98352382063
# 2    |    6.27266780189
# 3    |    5.61419869218
# 4    |    5.15532785565
# 5    |    4.82293522896
# 6    |    4.53860884822
# 7    |    4.32172743917
# 8    |    4.1031102396
# 9    |    3.93080551002
# 10    |    3.75552305045
# 11    |    3.62781776948

# WOW for the opposite reason! It looks like even more clusters might be better though, let's see what it looks like all the way up to k = 20:

cluster_list = range(2,21)
scores = [k_mean_score(k) for k in cluster_list]
# for k,score in enumerate(scores):
#     print "{}    |    {}".format(k+2,score)

# In [1]: run k_means_exploratory.py
# 2    |    10.3392710572
# 3    |    8.20782365542
# 4    |    6.99555239213
# 5    |    6.27123754677
# 6    |    5.61448709903
# 7    |    5.15500670003
# 8    |    4.87103152678
# 9    |    4.52969250461
# 10    |    4.28578790263
# 11    |    4.09964678513
# 12    |    3.89773639954
# 13    |    3.8014374653
# 14    |    3.66124535092
# 15    |    3.51342310644
# 16    |    3.40303715384
# 17    |    3.32218665601
# 18    |    3.19404891742
# 19    |    3.09723950391
# 20    |    3.07776821515

# OK...let's visualize this so we can maybe use the elbow method to choose a number of clusters

# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(1,1,1)
# ax.plot(cluster_list, scores, 'x--')
# ax.set_xlabel('K')
# ax.set_ylabel('Y')
# plt.savefig('../img/rss_over_k.png')
# plt.close()

# Not TOO helpful...let's try looking at some silhouette scores instead
scores = [k_mean_score(k,scoring='silhouette') for k in cluster_list]
for k,score in enumerate(scores):
    print "{}    |    {}".format(k+2,score)

# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(1,1,1)
# ax.plot(cluster_list, scores, 'x--')
# ax.set_xlabel('K')
# ax.set_ylabel('Silhouette Score')
# plt.savefig('../img/silhouettes_over_k.png')
# plt.close()

# Starting to get a little clarity here, it looks like k=10ish might be the sweet spot!  Let's look at some more indepth plotting - the cluster_and_plot function is taken (maybe?) from Frank Burkholder as part of his clustering lecture for Galvanize's DSI

# for i in cluster_list:
#     cluster_and_plot(X, i)

# We're still seeing scores level off around k=10, but graphing the scores really hammers home that our model simply isn't very good.  The silhouette scores appear too low to be fixed even by a thorough optimization of the model parameters, so it's time to search for a different model.
