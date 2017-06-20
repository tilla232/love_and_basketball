# Didn't realize until looking for previous season's stats that py_goldsberry doesn't work for seasons previous to this year's! (2016-17) Not usable!

import cPickle
import pandas as pd
import goldsberry
import string

def get_bbref(year):
    '''
    year = XXXX integer
    stats = list of stats you wish to cluster on, must be stats that are column names in the CSV
    '''
    bbref = pd.read_csv('../data/{}bbref.csv'.format(year))

    bbref_advanced = pd.read_csv('../data/{}bbref_advanced.csv'.format(year))

    # the format of this table, taken directly from basketball-reference.com, is a little annoying: the 'Player' column features a player's name, followed by his abbreviation that the site uses as a URL endpoint.  We don't need this bit, so this line strips it, and does a little additional cleaning

    bbref['Player'] = bbref['Player'].apply(lambda x: x.split('\\',1)[0].translate(None,string.punctuation.replace("'",'')).replace(' Jr','').replace('Jr.','').replace("III",'').strip())

    bbref.set_index('Player',inplace=True)

    # same cleaning process on advanced data
    bbref_advanced['Player'] = bbref_advanced['Player'].apply(lambda x: x.split('\\',1)[0].translate(None,string.punctuation.replace("'",'')).replace(' Jr','').replace('Jr.','').replace("III",'').strip())

    bbref_advanced.set_index('Player',inplace=True)

    # merge the datasets
    bbref = bbref.merge(bbref_advanced,how='outer',left_index=True,right_index=True)

    # drop extraneous columns
    bbref.drop(['Rk_x', 'Rk_y','Season_y','Age_y','Tm_y','Lg_y','G_y','MP_y','TS%_y','GS_y','MP.1_y'], axis=1, inplace=True)
    return bbref

# There are a few (extremely annoying) exceptions to the naming conventions on NBA.com.  bbref is very good about standardizing this, NBA is decidedly not....this section will fix these exceptions, this first line is an example of how to easily do this
# bbref.Player[99] = 'Nene'





def get_goldsberry(year):
    '''
    Input year as two-digit argument! (ie, 2016-17 = 16)
    '''
    players = goldsberry.PlayerList(Season='20{}-{}'.format(year,year+1))
    players = pd.DataFrame(players.players())
    players['DISPLAY_FIRST_LAST'] = players['DISPLAY_FIRST_LAST'].apply(lambda x: str(x).split('\\',1)[0].translate(None,string.punctuation.replace('-','').replace("'",'')).replace(' Jr','').replace('Jr.','').replace('III','').strip())

    player_dict = pd.Series(players['PERSON_ID'].values,index=players['DISPLAY_FIRST_LAST'])
    return player_dict


# now we see the reason for reading in the basketball-reference table: that table was built using the basketball-reference season finder, with parameters GP >= 50, and MPG >= 10.  This loop will remove all players from our player_dict that don't meet those criteria.

if __name__ == '__main__':
    year = 2015
    bbref = get_bbref_advanced(year)
    # player_dict = get_goldsberry(15)
    #
    # players_dict = {}
    # for player in bbref['Player'].values:
    #     players_dict[player] = player_dict[player]
    #
    # with open('../data/{}player_dict.txt'.format(year),'r+') as f:
    #     cPickle.dump(players_dict,f)
    # bbref.to_csv('{}bbref_advanced.csv')
