# Example of using PandasLoop
# Loops over pre-canned data in a dataframe
# Each column is a different stream (max 10 columns)

try:
    from credentials import ZOOBLAST_MOOSE as WRITE_KEY
except:
    print('You dont have a WRITE KEY')
    print('I am burning a really strong one now')
    from microprediction import new_key
    WRITE_KEY = new_key(difficulty=13)
    print(WRITE_KEY)
    raise Exception('Modify the code and do not lose the key above!')


from microprediction.looping import PandasLoop
import pandas as pd
import time

ORIGIN = 1641158602  # Epoch time you want to use for start
URL = 'https://raw.githubusercontent.com/microprediction/nba/main/data/games.csv'
FIELDS = ['FG_PCT','FG3_PCT','FT_PCT','DREB','REB','AST','STL','BLK','TOV','PF']


if __name__=='__main__':
    # Call this every day
    st = time.time()

    df = pd.read_csv(URL)
    df = df[FIELDS]
    renaming = dict([ (col,'basketball_'+col.lower()) for col in FIELDS])
    df = df.rename(columns=renaming)

    loop = PandasLoop(write_key=WRITE_KEY, interval=2, origin=1594147541, df=df, with_copulas=False)
    loop.run(minutes=23*60+58)

    hours_elapsed = (time.time()-st)/(60*60)
    print('Finished loop. Time elapsed is '+str(hours_elapsed))