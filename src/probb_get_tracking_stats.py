import requests
import os

import pandas as pd
import numpy as np

url = 'http://api.probasketballapi.com/sportsvu/player'
api_key = os.environ['PRO_BASKETBALL_API_KEY']
stats = ['cfga','cfgm','dist','spd','tchs','pass','sast','ftast','dfgm','dfga','rimd']

def request(season,player_id):
    query = {'api_key':api_key,'player_id':player_id}
    r = requests.post(url,data=query)
    df = pd.DataFrame(r.json())
    df = df[df['season'] == '{}'.format(season)]

    # for some reason, these stats are returned as objects - these lines convert them to floats
    df['dist'] = df['dist'].apply(lambda x: float(x))
    df['spd'] = df['spd'].apply(lambda x: float(x))

    df['rimd'] = df['dfgm']/df['dfga']
    df['rimd'] = df['rimd']*df['dfga']
    df = df[stats]

    return df

if __name__ == '__main__':
    season = 2016
    players = pd.read_csv('../data/{}player_ids.csv'.format(season))

    df = pd.DataFrame(index=players.player.values,columns=stats)

    for player,player_id in zip(players.player.values,players.id.values):
        player_stats = request(season,player_id)
        stats_dict = {}
        for stat in stats:
            stats_dict[stat] = player_stats.describe(include='all')[stat]['mean']
        df.loc[player] = stats_dict
    df.to_csv('../data/{}probb_tracking.csv'.format(season))
