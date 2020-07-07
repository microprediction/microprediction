from microprediction import MicroCrawler, new_key
from pprint import pprint
import muid


class DiracCrawler(MicroCrawler):

    def sample(self, lagged_values, **ignored):
        x = 0.5*lagged_values[0]+0.5*lagged_values[1]
        return [x]*self.num_predictions