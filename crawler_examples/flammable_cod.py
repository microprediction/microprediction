from microprediction import MicroCrawler
import numpy as np

class FlammableCod(MicroCrawler):

    " Example crawler ... this guy is likely to succeed only on z-streams, but helps the ecosystem by entering quickly "

    def __init__(self,write_key):
        super().__init__(stop_loss=50,min_lags=0,sleep_time=90,write_key=write_key)

    def candidate_streams(self):
        """ He'll try anything """
        return [name for name, sponsor in self.get_sponsors().items() ]

    def sample(self, lagged_values, lagged_times=None ):
        if len(lagged_values or [])>25:
            return super().sample(lagged_values=lagged_values, lagged_times=lagged_times )
        else:
            return sorted(np.random.randn(self.num_predictions))   # Not to bad for z-streams, terrible for most others


if __name__=="__main__":
    try:
        from microprediction.config_private import FLAMMABLE_COD
    except:
        raise Exception("You will need a write_key for this example to work  ")
    print(FLAMMABLE_COD)
    mw = FlammableCod(write_key=FLAMMABLE_COD)
    mw.run()




