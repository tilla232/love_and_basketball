import pandas as pd
import numpy as np
import timeit

import matplotlib.pyplot as plt

from sklearn.cluster import AgglomerativeClustering,SpectralClustering,Birch,DBSCAN,KMeans

from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score,pairwise
from sklearn.neighbors import kneighbors_graph

def get_data(df,stats_list):
    '''
    Takes in final stats dataframe and stats list in format of the list seen in the main block below, outputs normalized data (X) - also outputs team column (tm) for future reattachment
    '''
    X = df.set_index('player_year')
    tm = X.pop('Tm_x')

    X = X[stats_list]

    # one column (3Par) has a few nans - it makes sense to simply convert these to 0's
    X.fillna(value=0,inplace=True)

    X = normalize(X)
    return X,tm

def print_silhouette_scores(X,cluster_list,affinity_list,neighbors_list):
    print ('k | n')
    x = (0,0,0)
    for n in neighbors_list:
        knn_graph = kneighbors_graph(X,n)
        for k in cluster_list:
            model = AgglomerativeClustering(n_clusters=k,connectivity=knn_graph,linkage='complete')
            model.fit(X)
            print ('{} | {}    |    {}'.format(k,n,silhouette_score(X,model.labels_)))

def plot_silhouette_scores(X,cluster_list):
    '''
    Takes fit model and range of number of clusters and plots silhouette score of each number of clusters, saves plots in img folder
    '''
    x,y = [],[]
    for n in cluster_list:
        spectral = SpectralClustering(n_clusters=n,n_init=1000,n_jobs=2,linkage='average')
        spectral.fit(X)
        x.append[n],y.append[silhouette_score(X,spectral.labels_)]
    plt.plot(x,y)
    plt.xlabel('N Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Spectral Clustering with Discretization for Label Assignment')
    plt.savefig('../img/spectral_silhouettes.png')
    plt.close()




if __name__ == '__main__':
    # Initialization Options
    new_stats_list = ['FG','FGA','2P','2PA','3P','3PA','FT','FTA','ORB','DRB','AST','STL','BLK','3PAr','FTr','ORB%','DRB%','AST%','STL%','BLK%','USG%','DRtg','DWS','DBPM','dist','spd','tchs','pass','sast','ftast','dfgm','dfga']

    df = pd.read_csv('../data/final_stats.csv')
    cluster_list = range(5,21)
    affinity_list = ['euclidean','l1','l2','manhattan','cosine']
    gamma_list = np.linspace(0.1,1,10)
    neighbors_list = np.arange(30,100,10)
    threshold_list = np.linspace(0.01,0.25,10)
    algorithm_list = ['auto','ball_tree','kd_tree','brute']


    X,tm = get_data(df,new_stats_list)
    km = KMeans(n_clusters=13,max_iter=500,n_init=23,algorithm='full',precompute_distances=True,n_jobs=3,verbose=5)
    # print_silhouette_scores(X,stats_list,affinity_list,neighbors_list)

    # agglomerative optimizer
    # max_score_vector = (0,0,0,0)
    # agg_df = pd.DataFrame

    # for n in neighbors_list:
    #     knn_graph = kneighbors_graph(X,n)
    #     for k in cluster_list:
    #         for a in affinity_list:
    #             model = AgglomerativeClustering(n_clusters=k,connectivity=knn_graph,linkage='average',affinity=a)
    #             model.fit(X)
    #             print ('{} | {} | {}   |    {}'.format(k,n,a,silhouette_score(X,model.labels_)))
    #             if silhouette_score(X,model.labels_) > max_score_vector[2]:
    #                 max_score_vector = (k,n,a,silhouette_score(X,model.labels_))

    # # spectral optimizer
    # max_score_vector = (0,0,0,0)
    # spectral_df = pd.DataFrame(index=range(160),columns=['g','k'])

    # n = 0
    # for g in gamma_list:
    #     for k in cluster_list:
    #         model = SpectralClustering(n_clusters=k,affinity='rbf',gamma=g,n_init=500,n_jobs=2)
    #         model.fit(X)
    #         print ('{} | {}   |    {}'.format(k,g,silhouette_score(X,model.labels_)))
    #
    #         spectral_df.loc[n] = {'g':g,'k':k}
    #
            # if silhouette_score(X,model.labels_) > max_score_vector[2]:
            #     max_score_vector = (k,g,silhouette_score(X,model.labels_))
    #
    #         n += 1

    # BIRCH optimizer
    # max_score_vector = (0,0,0)
    # n = 0
    # for t in threshold_list:
    #     for k in cluster_list:
    #         model = Birch(threshold=t,n_clusters=SpectralClustering(n_clusters=k,n_init=500,n_jobs=3),branching_factor=100)
    #         model.fit(X)
    #         print ('{}|{}    |    {}'.format(t,k,silhouette_score(X,model.labels_)))
    #
    #         if silhouette_score(X,model.labels_) > max_score_vector[2]:
    #             max_score_vector = (t,k,silhouette_score(X,model.labels_))
    #         n += 1

    # DBSCAN optimizer
    # max_score_vector = (0,0,0)
    # n = 0
    # similarity = pairwise.cosine_similarity(X)
    # for epsilon in np.linspace(0.01,0.25,10):
    #     for a in algorithm_list:
    #         model = DBSCAN(eps=epsilon,algorithm=a,leaf_size=50,n_jobs=3,min_samples=10)
    #         model.fit(similarity)
    #         score = 0
    #         try:
    #             score = silhouette_score(X,model.labels_)
    #         except ValueError:
    #             pass
    #         print ('{}|{}    |    {}'.format(epsilon,a,score))
    #
    #         if score > max_score_vector[2]:
    #             max_score_vector = (t,k,score)
    #         n += 1
