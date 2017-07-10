  
# A Winning Formula  
Note: This repo is still (very much) under construction!  Optimizations for some of the clustering methods used in this study can be found in jupyter notebooks in the src directory, along with a number of python scripts used to pull data.

## Table of Contents  
1. [Abstract](#abstract)  
2. [Data](#data)  
3. [Clustering](#clustering)
    * [K-Unspecified](#k-unspecified)
        * [DBSCAN](#dbscan)
        * [BIRCH](#birch)
        * [Affinity Propagation](#affinity-propagation)
    * [K-Specified](#k-specified)
        * [K-Means](#k-means)
        * [Gaussian Mixture Model](#gaussian-mixture-model)
        * [Agglomerative Clustering](#agglomerative-clustering)

  
## Abstract

There’s long been a simmering belief that basketball’s traditional positional labels
(point guard, shooting guard, small forward, power forward, center) are insufficient in
fully describing a player’s role and activity on the court. Today, more than ever, the
issue is bubbling over, and we see players like Giannis Antetokounmpo, Nikola Jokic, et
al. bending the rules ascribed to players of their position by traditionalists - we need to
adapt our viewing/analyzing paradigms accordingly. [Muthu Alagappan famously made
an effort to reposition NBA players at Sloan 2012](http://www.sloansportsconference.com/wp-content/uploads/2012/03/Alagappan-Muthu-EOSMarch2012PPT.pdf), but his analysis falls short for me.
The main issue I find is that a number of his positions fail to impart any sense of how
the players of that position actually play on the floor, the most egregious among them,
‘role players’, being a position comprised of roughly the same number of players as
about *five* other positions combined. In all, a rough visual estimate tells me that, in this
analysis, roughly one-third of all NBA players wind up in this ‘role player’ position; this
is problematic, to say the least.

My aim in this study was initially in two parts - first, redefine player positions using advanced statistics and unsupervised machine learning (namely clustering), second, use these new positions for further analysis and predictive modeling.  Data constraints and other factors led to my inability to truly pursue the latter, but this ended up for the best.  I pivoted to a clustering-based, purely exploratory look at my data, learning a good deal about a variety clustering algorithms, and, most importantly, about basketball analysis.
  
  
## Data
  
Most of my data was pulled from [Basketball Reference](http://basketball-reference.com) - the site has a handy 'Get Table as CSV' option which made pulling the data a snap: 
![basketball reference](https://github.com/tilla232/dsi_capstone/blob/master/img/bbref.png?raw=true)  

I pulled not only per 36 minutes stats, but also advanced stats for each qualified player-season over the last 3 years.  A player-season was qualified if the player played at least 50 games and at least 10 minutes/game for that season.  Both the playing time constraint and the 3 season constraint were fairly restrictive, but ultimately necessary.  The playing time minimum was needed to limit noise, while the 3 season limit was intended to ensure my models would capture the positions of *today's* game.  
  
To bolster my data, I also used [ProBasketball API](https://probasketballapi.com/) to get data for a number of tracking statistics - total touches per game, distance covered per game, etc.  

My final data spanned 911 player-seasons and 53 statistics.  
   
## Clustering  
Clustering is a messy matter to begin with - in this study, its almost enigmatic nature was only exacerbated regardless of model selection and parameter tuning.  Our model is built around NBA players, almost none of whom are abjectly *terrible* at any one aspect of the game.  We would expect players from cluster 1 to be at least serviceable when it comes to the skills that players from cluster 2 thrive at, etc.  This fact alone made it hard to quantify success in my clustering, as we would almost expect something like mean silhouette score to have a fairly low cap. 

### K-Unspecified
#### DBSCAN
##### [Jupyter Notebook](src/dbscan_optimize.ipynb)

#### BIRCH
##### [Jupyter Notebook](src/birch_optimize.ipynb)

#### Affinity Propagation
##### [Jupyter Notebook](src/affinity_optimize.ipynb)

### K-Specified

#### K-Means
##### [Jupyter Notebook](src/kmeans_optimize.ipynb)

#### Gaussian Mixture Model
##### [Jupyter Notebook](src/gaussian_optimize.ipynb)

#### Agglomerative Clustering
##### [Jupyter Notebook](src/agglomerative_optimize.ipynb)

