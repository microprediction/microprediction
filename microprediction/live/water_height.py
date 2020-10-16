import pandas as pd


def height():
    df = pd.read_csv('https://www.ndbc.noaa.gov/data/realtime2/21413.dart')
    return float(df.iloc[1,:].values[0].split(' ')[-1])


if __name__=='__main__':
    print("Water height is "+str(height()))