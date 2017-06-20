import pandas as pd

df2016 = pd.read_csv('../data/2016stats.csv')
df2015 = pd.read_csv('../data/2015stats.csv')
df2014 = pd.read_csv('../data/2014stats.csv')

df2016['player_year'] = df2016.Player.map(str) + '/' +  df2016['Season_x'].map(str)
df2015['player_year'] = df2015.Player.map(str) + '/' +  df2015['Season_x'].map(str)
df2014['player_year'] = df2014.Player.map(str) + '/' +  df2014['Season_x'].map(str)

df2016.set_index('player_year',inplace=True)
df2015.set_index('player_year',inplace=True)
df2014.set_index('player_year',inplace=True)

all_stats = pd.concat([df2016,df2015,df2014])

all_stats.to_csv('../data/final_stats.csv')
