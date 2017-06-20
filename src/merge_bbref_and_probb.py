import pandas as pd
from create_player_dict import get_bbref

def merge(season):
    bbref = get_bbref(season)
    probb = pd.read_csv('../data/{}probb_tracking.csv'.format(season))

    probb.set_index('Unnamed: 0',inplace=True)
    probb.sort_index(inplace=True)

    df = bbref.merge(probb,left_index=True,right_index=True)
    return df

if __name__ == '__main__':
    df2016 = merge(2016)
    df2015 = merge(2015)
    df2014 = merge(2014)

    # fix Quincy Acy stats when you want to cluster
    # df2016.to_csv('../data/2016stats.csv')
    # df2015.to_csv('../data/2015stats.csv')
    # df2014.to_csv('../data/2014stats.csv')
