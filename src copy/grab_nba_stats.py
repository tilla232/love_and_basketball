import cPickle
import pandas as pd
import nba_py.player as nba
from time import sleep
from random import randint
import numpy as np

# This is totally functional! But really slow, and, as I'm only getting one stat at a time, super inefficient.
def get_rim_defense(playerID):
    num = randint(20,40)
    print num

    player_defense = nba.PlayerDefenseTracking(playerID)
    player_defense.json.pop('parameters')
    player_defense.json.pop('resource')

    sleep(num)
    return player_defense.json['resultSets'][0]['rowSet'][3][9]


# FIX THIS!! if you want to populate the DF inside the function, you have to do it entry-by-entry
def get_shot_stats(playerID,n):
    num = randint(15,40)
    print n , player_dict.keys()[player_dict.values().index(playerID)], 'getting shooting stats!'
    idx = players[players.id == playerID].index[0]

    player_shooting = nba.PlayerShotTracking(playerID).general_shooting()

    # catch and shoot 3 point shooting metric
    catchshoot = player_shooting[player_shooting.SHOT_TYPE == 'Catch and Shoot']
    if catchshoot.empty:
        players.set_value(idx,'3catch_and_shoot',0.0)
        return

    catch_and_shoot3 = catchshoot.FG3A_FREQUENCY[0] * catchshoot.FG3M[0]
    players.set_value(idx,'3catch_and_shoot',catch_and_shoot3)

    # pull-up shooting metric
    pullups = player_shooting[player_shooting.SHOT_TYPE == 'Pull Ups']
    if pullups.empty:
        players.set_value(idx,'pullupshoot',0.0)
        return

    pullupshoot = pullups.EFG_PCT[1] * pullups.FGA[1]
    players.set_value(idx,'pullupshoot',pullupshoot)


    sleep(num)

def get_rebound_stats(playerID):
    num = randint(10,20)
    print num , 'getting rebounding stats!'
    idx = players[players.id == playerID].index[0]

    player_rebounding = nba.PlayerReboundTracking(playerID).rebound_distance_rebounding()

    paint_rebounding = player_rebounding[0:2]
    contested_paint = paint_rebounding.C_REB_PCT[0] * paint_rebounding.C_REB_PCT[1]
    players.set_value(idx,'paint_rebounding',contested_paint)

    sleep(num)

# I don't see anything I need in the PlayerPassTracking class...for now...
# def get_passing_stats(playerID):
#     num = randint(10,20)
#     print num , 'getting passing stats!'
#     idx = players[players.id == playerID].index[0]
#
#     player_passing = nba.PlayerPassTracking(playerID)







if __name__ == '__main__':
    with open('../data/player_dict.txt','r+') as f:
        player_dict = cPickle.load(f)

    players = pd.DataFrame(player_dict.items(),columns=['player','id'])


    # players['rim_defense'] = players['id'].apply(lambda x: get_rim_defense(x))

    players['3catch_and_shoot'] = np.nan
    players['pullupshoot'] = np.nan
    players['paint_rebounding'] = np.nan

    n = 0
    for player_id in players.id.values:
        get_rebound_stats(player_id)
