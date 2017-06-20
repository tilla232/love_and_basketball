import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import seaborn as sns

from agglomerative import get_data

from sklearn.manifold import TSNE
from sklearn import feature_selection as fs
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, Birch, MeanShift,AffinityPropagation
from sklearn.metrics import silhouette_score

def plot_tsne_scatter(X,filename=None,three_d=False,title=None):
    '''
    Arguments:
    X - Feature matrix X, a dataframe or array of numerical data.
    filename - String, appended to filename of png written to directory img
    three_d - Boolean, if True, function plots and saves 3-d representation of data as well.
    title - String, used as title of plot(s)

    Output:
    None, plots 2d-projection of higher-dimensional data, saves figure to img directory.
    '''
    tsne2d = TSNE(n_components=2,init='pca',random_state=23).fit_transform(X)
    tsne3d = TSNE(n_components=3,init='pca',random_state=23).fit_transform(X)


    fig = plt.figure(figsize=(6,4))
    ax1 = fig.add_subplot(111)
    ax1.scatter(tsne2d[:,0],tsne2d[:,1],cmap=plt.cm.Spectral)
    ax1.set_title(title)
    plt.axis('tight')
    if not filename:
        plt.savefig('../img/2dtsne.png')
    else:
        plt.savefig('../img/2dtsne_{}.png'.format(filename))

    if three_d:
        ax2 = fig.add_subplot(111,projection='3d')
        ax2.scatter(tsne3d[:,0],tsne3d[:,1],tsne3d[:,2],cmap=plt.cm.Spectral)
        ax2.set_title(title)
        plt.axis('tight')
        if not filename:
            plt.savefig('../img/3dtsne.png')
        else:
            plt.savefig('../img/3dtsne_{}.png'.format(filename))

def tsne_silhouette_score(X,mod='KMeans'):
    tsne = TSNE(n_components=2,init='pca',random_state=23)
    tsne.fit(X)
    tsne_vectors = tsne.embedding_

    if mod == 'KMeans':
        model = KMeans(n_clusters=5) # 5 because 5 NBA positions, get it?!
    if mod == 'AffinityPropagation':
        model = AffinityPropagation()

    model.fit(tsne_vectors)

    return silhouette_score(tsne_vectors,model.labels_)

def randomize_feature_space(stats_list):
    no_features = random.randint(10,53)
    features_index = random.sample(range(0,53),no_features)

    return [stats_list[x] for x in features_index]


if __name__=='__main__':
    stats_list = ['MP_x','FG','FGA','2P','2PA','3P','3PA','FT','FTA','ORB', 'DRB', 'TRB', 'AST', 'STL','BLK','TOV','PF','PTS','FG%','2P%','3P%', 'eFG%', 'FT%', 'TS%_x', 'PER', '3PAr','FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%','ORtg', 'DRtg', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM','VORP', 'dist', 'spd', 'tchs', 'pass', 'sast', 'ftast', 'dfgm','dfga']

    df = pd.read_csv('../data/final_stats.csv')

    X,tm = get_data(df,stats_list)

    # plot_tsne_scatter(X)
    # we see...nothing resembling discernible clusters - let's try some feature reduction
    # t_list = np.linspace(0.2,0.99,20)[::-1]
    # for t in t_list:
    #     try:
    #         variance = fs.VarianceThreshold(threshold=t)
    #         break
    #     except ValueError:
    #         continue
    # X = variance.fit_transform(X)
    # X = normalize(X)
    #
    # # plot_tsne_scatter(X,filename='var_threshold')
    # idx = variance.get_support(indices=True)
    # new_stats_list = [stats_list[idx[i]] for i,_ in enumerate(idx)]
    # new_stats_list = ['2P','2PA','3P','3PA','FT','FTA','ORB','DRB','AST','STL','BLK','dist','tchs','pass','sast','ftast','dfgm','dfga']
    # #,'ORB%','DRB%','AST%','STL%','BLK%','USG%'
    # X,tm = get_data(df,new_stats_list)
    # X = normalize(X)
    # plot_tsne_scatter(X,filename='reduced2')

    # Let's randomize our feature space, and check the silhouette score when we cluster on the resulting TSNE embedding vectors!
    # n = 0
    # feature_space_dict = {}
    # for i in range(4):
    #     potential_features = []
    #     max_vect = ([],0)
    #     for _ in range(500):
    #         new_stats = randomize_feature_space(stats_list)
    #         X, _ = get_data(df,new_stats)
    #         score = tsne_silhouette_score(X,mod='KMeans')
    #         potential_features.append((new_stats,score))
    #         if n % 25 == 0:
    #             print n
    #         n += 1
    #
    #     potential_features.sort(key=lambda x: x[1])
    #     print potential_features[-1]
    #     feature_space_dict[i] = potential_features[-1]

    # The best we did here with 20 iterations was a silhouette score around .45, let's try to do better! Set it to 500 iterations, and go for a coffee break...
    # Not much better, .45ish appears to be our peak...let's try some unsupervised clustering instead (KMeans -> Affinity Propagation)!

    #     In [2]: run cluster_visual.py
    # (['FG%', 'TOV', '3P%', 'DBPM', '3PA', 'BLK', 'STL', 'STL%', '2P%', 'dfgm', 'dfga', '3PAr', 'AST%', 'FT%'], 0.48871119638648813)
    # # Maybe that's the best we'll do? Let's look at the TSNE plot of these features...
    # new_feature_space = ['DRtg', 'eFG%', 'pass', 'FT%', 'tchs', '3PA', 'STL', 'dfgm', '3PAr', 'TRB', 'BLK', 'OBPM', 'FT']
    # X,tm = get_data(df,new_feature_space)
    # # plot_tsne_scatter(X,filename='new_feature_space',title='TSNE')
