import pandas as pd
from pprint import pprint
from microprediction import PandasLoop, new_key
import time

def example_df():
    df = pd.DataFrame(columns=['x','y'], data=zip(list(range(12000)),list(range(12000))))
    return df

def test_current_row():
    df = example_df()
    write_key = new_key(difficulty=7)
    loop = PandasLoop(df=df,origin=time.time(), interval=0.1, write_key=write_key)
    assert loop._current_row()==0
    assert loop.current_values()[0]==0
    time.sleep(7)
    assert loop._current_row() == 1
    assert loop.current_values()[0] == 1
    time.sleep(7)
    assert loop._current_row() == 2
    assert loop.current_values()[0] == 2


def test_values():
    df = example_df()
    write_key = new_key(difficulty=7)
    loop = PandasLoop(df=df, origin=time.time(), interval=0.1, write_key=write_key)
    for k in range(10):
        assert loop._values(k=k)[0]==k

