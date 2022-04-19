from microprediction import MicroCrawler
import numpy as np

try:
   from credentials import BOOZE_MAMMAL as WRITEKEY
except ImportError:
   raise EnvironmentError('You need a write key, explained at https://www.microprediction.com/private-keys')


class BoozeMammal(MicroCrawler):

    """Example crawler ... z-streams only and predicts slightly fatter tails
       Nassim Taleb educated me https://www.youtube.com/watch?v=A72cc8mM5gY
       Could a few lines of code save humanity from thin tails ?!
       It sure is worth a try.
    """

    def __init__(self,write_key):
        super().__init__(stop_loss=10,min_lags=0,sleep_time=15*60,write_key=write_key,quietude=1,verbose=False)

    def excluce_sponsor(self,sponsor,**ignore):
        return sponsor.lower() == 'doomsday stoat'       # Avoid the DOOM

    def candidate_streams(self):
        return [name for name, sponsor in self.get_stream_names() if (name[:2]=='z1') ]

    def sample(self, lagged_values, lagged_times=None, **ignore ):
        """ Fat tails """
        return [1.02*s*(1+0.1*abs(s)) for s in sorted(np.random.randn(self.num_predictions)) ]  # Not to bad for z1-streams, terrible for most others

if __name__=="__main__":
    mw = BoozeMammal(write_key=WRITE_KEY)
    mw.set_repository('https://github.com/microprediction/microprediction/blob/master/submission_examples_independent/booze_mammal.py')
    mw.run()






