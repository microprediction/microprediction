# Illustrates a crawler that performs incremental estimation
from microprediction import MicroCrawler
import time
from collections import OrderedDict

class OnlineHorizonCrawler(MicroCrawler):

    # Crawler maintains a queue of horizons and cycles through them, calibrating as it goes
    # To use this crawler, override the initial_state() and update_state() methods
    # These store state keyed by horizon so your sample() method can make use of the state conveniently

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = OrderedDict()  # Maintains an ordered list of state objects indexed by horizon

    ################################################################################
    #  Override these methods                                                      #
    ################################################################################

    def initial_state(self, name, delay=None, **ignore):
        """ How do you want state initialized? """
        return None

    def update_state(self, state, **ignore):
        return state

    ################################################################################
    #   Maybe don't override the methods below unless you know what you are doing  #
    ################################################################################

    def add_active_to_queue(self):
        """ Ensure there is a state object for each horizon """
        # You may want to change this to have a state object for each stream instead
        for horizon in self.get_active():
            if not horizon in self.queue:
                name, delay = self.split_horizon_name(horizon)
                self.queue.update({horizon:self.initial_state(name=name,delay=delay)})

    def downtime(self,seconds,**ignored):
        """ During downtime we cycle through the state and update it """
        self.add_active_to_queue()
        start_time = time.time()
        while time.time()< start_time+seconds-5:
            if self.queue:
                state_key, state = self.queue.popitem(0)
                state = self.update_state(state)
                self.queue.update({state_key:state})
                time.sleep(3)


class OnlineStreamCrawler(OnlineHorizonCrawler):

    # Crawler maintains a queue of streams and cycles through them, calibrating as it goes
    # To use this crawler, override the initial_state() and update_state() methods
    # These store state keyed by name so your sample() method can make use of the state conveniently

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = OrderedDict()  # Maintains an ordered list of state objects indexed by stream name

    ################################################################################
    #  Override these methods                                                      #
    ################################################################################

    def initial_state(self, name, **ignore):
        """ How do you want state initialized? """
        return None

    def update_state(self, state, **ignore):
        return state

    ################################################################################
    #   Maybe don't override the methods below unless you know what you are doing  #
    ################################################################################

    def add_active_to_queue(self):
        """ Ensure there is a state object for each horizon """
        # You may want to change this to have a state object for each stream instead
        active_streams = [ self.split_horizon_name(horizon)[0] for horizon in self.get_active() ]
        for name in active_streams:
            if not name in self.queue:
                self.queue.update({name:self.initial_state(name)})


