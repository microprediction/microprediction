import pandas as pd

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started creating streams (see the 4th module in particular)


def height():
    df = pd.read_csv('https://www.ndbc.noaa.gov/data/realtime2/21413.dart')
    return float(df.iloc[1,:].values[0].split(' ')[-1])


if __name__=='__main__':
    print("Water height is "+str(height()))