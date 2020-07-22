# Simple crawler on curated streams and delays to get you started
from microprediction.crawler import MicroCrawler

CURATED = ['bart_delays.json','altitude.json','traffic_absolute_speed.json','hospital_bike_activity.json',
          'badminton_x.json','helicopter_theta.json','seattle_wind_direction.json','seattle_wind_speed.json',
          'three_body_z.json','pandemic_infected.json','goog.json']   #TODO: Replace with featured list API


class SimpleCrawler(MicroCrawler):

    """ A crawler that just make 1-step ahead predictions on a subset of streams """
    # See crawler_examples/simplecrawler.py for usage example

    def __init__(self, **kwargs):
        """ """
        super().__init__(**kwargs)

    def include_stream(self, name=None, **ignore):
        return name in CURATED

    def exclude_stream(self, name=None, **ignore):
        """ Tell it to ignore bivariate and trivariate prediction streams """
        return '~' in name

    def include_delay(self, delay=None, name=None, **ignore):
        """ Tell it to only worry about the next data point, for simplicity """
        return delay<90





class RegularCrawler(MicroCrawler):

    " Only hits regular streams, not bivariate or trivariate """

    def __init__(self,write_key=None,**kwargs):
        super().__init__(write_key=write_key,**kwargs)

    def exclude_stream(self, name=None, **ignore):
        return '~' in name