from microprediction.config_private import BOOZE_MAMMAL
from microprediction import MicroCrawler
import numpy as np

# Need help? New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

class BoozeMammal(MicroCrawler):

    """Example crawler ... z-streams only and predicts slightly fatter tails
       I was able to write this only after Nassim Taleb educated me https://www.youtube.com/watch?v=A72cc8mM5gY
       Could a few lines of code save humanity from thin tails ?!
       It sure is worth a try.
    """

    def __init__(self,write_key):
        super().__init__(stop_loss=10,min_lags=0,sleep_time=15*60,write_key=write_key,quietude=1,verbose=False)

    def candidate_streams(self):
        return [name for name, sponsor in self.get_sponsors().items() if name[:2]=='z1' ]

    def sample(self, lagged_values, lagged_times=None, **ignored ):
        """ Fat tails """
        return [1.02*s*(1+0.1*abs(s)) for s in sorted(np.random.randn(self.num_predictions)) ]  # Not to bad for z1-streams, terrible for most others

if __name__=="__main__":
    mw = BoozeMammal(write_key=BOOZE_MAMMAL)
    mw.run()




