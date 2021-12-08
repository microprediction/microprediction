from microprediction import MicroCrawler
from keys import STOOF_EAGLE
import numpy as np
import pandas as pd
import random

class MyCrawler(MicroCrawler):

    def __init__(self, **kwargs):
        super().__init__( **kwargs)

    def candidate_streams(self):

        names = [ n for n in self.get_stream_names()]

        return names


    def sample(self, name, lagged_values, lagged_times=None, **ignored):
        if len(set(lagged_values)) > (len(lagged_values) ** 0.5):
            return

        if 'meme' in name:
            p = 0.8

        if 'p' in locals():
            last_value = lagged_values[-1]
            past_values = [v for v in lagged_values if v != last_value]

            table = pd.Series(past_values)
            multiplier = np.floor(table.value_counts().sum() * p / (1-p))

            dist = past_values + [last_value] * int(multiplier)

        else:
            dist = lagged_values

        while len(dist) < 225:
            dist = dist + dist

        submissions = random.sample(dist,225)

        scaled_subs = []
        for s in submissions:
            while s > 10 ** 7:
                s = s / 100
            scaled_subs.append(s)

        rand_scaled_subs = [s + (0.0000000001 * np.random.rand()) for s in scaled_subs]

        return rand_scaled_subs


if __name__ == "__main__":

    mw = MyCrawler(write_key=STOOF_EAGLE, min_lags=50, max_active=1000, quietude=1, verbose=False)
    mw.set_repository(url='https://github.com//microprediction/microprediction/blob/master/crawler_examples/stoof_eagle.py')
    mw.run(withdraw_all=False)