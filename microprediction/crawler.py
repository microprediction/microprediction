# Provides an example of a self-navigating algorithm which you are under no obligation to use

from microprediction.writer import MicroWriter
import muid, random, time
from microprediction.samplers import exponential_bootstrap
import pprint

class MicroCrawler(MicroWriter):

    def __init__(self, write_key=None, base_url="http://www.microprediction.com/", verbose=True, min_lagged=50, min_difficulty=12) :
        """ Initialize write_key if none provided """
        super().__init__(base_url=base_url, write_key=write_key )
        assert muid.difficulty(write_key) >= 8, "Invalid write_key for crawler. See www.muid.org to mine one. "
        self.verbose = verbose
        self.min_lagged = min_lagged          # Only consider streams with a long lag history
        self.min_difficulty = min_difficulty  # Only choose streams with sponsors at least this long

    def choose_stream(self):
        """ Randomized """
        streams = self.get_streams()
        candidates = [ name for name, sponsor in streams.items() if len(sponsor.replace(' ',''))>=self.min_difficulty ]
        return random.choice(candidates)

    def choose_horizon(self):
        return random.choice(self.delays)

    def run(self):
        while True:
            name  = self.choose_stream()
            delay = self.choose_horizon()
            lagged = self.get_lagged_values(name)
            if len(lagged)<self.min_lagged:
                message = {'name':name,'submitted':False,"lagged_len":len(lagged)}
            else:
                scenario_values = exponential_bootstrap(lagged=lagged,num=self.num_predictions, decay=0.01)
                self.submit(name=name,values=scenario_values,delay=delay)
                balance = self.get_balance()
                errors  = self.get_errors()
            if self.verbose:
                message = {'name':name,"submitted":True, "balance":balance,"errors":errors[:5],'delay':delay,"values":scenario_values[:5],}
                pprint.pprint(message)
                print("",flush=True)
            time.sleep(300)





