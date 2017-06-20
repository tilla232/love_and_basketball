  
# A Winning Formula    

## Table of Contents  
1. [Abstract](#abstract)  
2. [Data](#data)  
3. [Clustering](#clustering)
    * [K-Unspecified](#k-unspecified)
    * [K-Specified](#k-specified)
    

  
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
  
Data was pulled from [Basketball Reference](http://basketball-reference.com) - the site has a handy 'Get Table as CSV' option which made pulling/using this data a snap: 
![basketball reference](https://github.com/tilla232/dsi_capstone/blob/master/img/bbref.png?raw=true)  

The site makes it incredibly easy not only to pull common counting stats for every player in a given season, but also to find the more advanced stats - those that lend a bit more insight into how a player actually spends his time on the floor.
   
## Clustering  
### K-Unspecified
Clustering is a messy matter to begin with, and was only further complicated, in this study, by the cluster overlap we would almost inherently find, regardless of model selection and parameter tuning.  Our model is built around NBA players, almost none of whom are abjectly *terrible* at any one aspect of the game.  We would expect players from cluster 1 to be at least serviceable when it comes to the skills that players from cluster 2 thrive at, etc.  This fact alone made it hard to quantify success in our clustering, as we would almost expect something like mean silhouette score to have a fairly low cap. 

I was initially using roughly 20 features to cluster upon, and decided some dimensionality reduction could help improve my model's performance.  After some tinkering with sklearn's PCA class, I quickly realized that a dramatic reduction in dimension (n_components = 2) was drastically boosting my silhouette scores, but producing a set of clusters where some made perfect sense, but others were...hard to explain, from a basketball standpoint.   
![cluster snippet](https://github.com/tilla232/dsi_capstone/blob/master/img/cluster_snippet.png?raw=true)  
  
 
I suspected that such intense dimension reduction was making my clustering model cluster based on overall contribution - in a sense, the PCA was effectively calculating an overall performance metric (stats like VORP, WS, BPM, etc.) on the fly; this was decidedly *not* what I was trying to accomplish.  
  
  
~~While these clusters made sense to me, I wanted to quantify them *somehow*, for the sake of both science as well as sanity-checking...I obtained simple numerical data (mean and range) for each feature, for each cluster - this also proved useful in *qualifying* each cluster, as it becamse immediately apparent what skills each cluster exemplified.~~

### K-Specified


