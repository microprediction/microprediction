## OnlineCrawler

The [OnlineHorizonCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/onlinecrawler.py) and 
[OnlineStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/onlinecrawler.py) are minor tweaks on 
MicroCrawler offer an interface where the only thing one needs to override


    def initial_state(self, name, delay=None, **ignore):
        """ How do you want state initialized? """
        return None

    def update_state(self, state, **ignore):
        return state

The OnlineHorizonCrawler maintains a queue of horizons and cycles through them, calibrating as it goes. As the name suggests the state is keyed by horizon (i.e. a choice of stream plus a forecast length). If you wish to store the same state for each of the four prediction horizons (i.e. on
state for each stream) then use the OnlineStreamCrawler. 

### Hierarchy

Don't like this pattern? Back up to [predict using MicroCrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html).


     MicroReader
         |
     MicroWriter
         |
     MicroCrawler
         | 
     OnlineHorizonCrawler
         |
     OnlineStreamCrawler
     

-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)


