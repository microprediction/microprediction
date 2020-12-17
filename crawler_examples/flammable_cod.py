from microprediction import MicroCrawler
import numpy as np

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

class FlammableCod(MicroCrawler):
    " Example crawler ... this guy helps flush the pipes by entering quickly and getting out quickly "

    def __init__(self, write_key, **kwargs):
        super().__init__(stop_loss=2, min_lags=1, sleep_time=5, write_key=write_key, quietude=1, verbose=False,
                         **kwargs)

    def candidate_streams(self):
        """ He'll try anything """
        return [name for name, sponsor in self.get_sponsors().items()]

    def sample(self, lagged_values, lagged_times=None, **ignore):
        if len(lagged_values or []) > 25:
            return super().sample(lagged_values=lagged_values, lagged_times=lagged_times)
        else:
            return sorted(np.random.randn(self.num_predictions))  # Not to bad for z-streams, terrible for most others


if __name__ == "__main__":
    try:
        from microprediction.config_private import FLAMMABLE_COD
        mw = FlammableCod(write_key=FLAMMABLE_COD)
        mw.set_repository(
            'https://github.com/microprediction/microprediction/blob/master/crawler_examples/flammable_cod.py')
    except ImportError:
        mw = FlammableCod(difficulty=10)
    print(mw.animal,flush=True)
    mw.run()
