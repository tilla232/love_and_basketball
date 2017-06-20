import requests
import os
import json
import pandas as pd
import numpy as np
import string
from create_player_dict import get_bbref


url = 'http://api.probasketballapi.com/player'
api_key = os.environ['PRO_BASKETBALL_API_KEY']

def request():
    '''
    Give season parameter as a 4 digit STRING - eg; the 2014-15 season would be entered '2014'
    '''
    query = {'api_key':api_key}
    r = requests.post(url, data=query)
    r = r.json()
    return r

if __name__ == '__main__':
    season = 2015
    bbref = get_bbref(season)
    bbref = bbref.index

    players = request()
    player_id_dict = {}

    for p in players:
        player_id_dict[p['player_name']] = p['id']

    df = pd.DataFrame()
    df['player'] = player_id_dict.keys()
    df['id'] = player_id_dict.values()

    # fixing annoying naming hangups
    df.player[df[df.player == 'Nene'].index[0]] = 'Nene Hilario'
    df.player[df[df.player == 'Taurean Prince'].index[0]] = 'Taurean WallerPrince'

    # more generic cleaning to standardize player names
    df['player'] = df['player'].apply(lambda x: str(x).translate(None,string.punctuation.replace("'",'')).replace(' Jr','').replace('Jr.','').replace("III",'').strip())

    for player in df.player.values:
        if player not in bbref:
            print player
            idx = int(df[df['player'] == player].index[0])
            df.drop([idx],inplace=True)

    df.to_csv('../data/{}player_ids.csv'.format(season))
