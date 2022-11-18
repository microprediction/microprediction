## Crawling

The MicroCrawler class, found in [micropredicton/crawler](https://github.com/microprediction/microprediction/blob/master/microprediction/crawler.py) is intended to
make it easier to shauffeur algorithms from one stream to the next. 

### Running the default crawler
Not a terrible way to get familiar with the system. 

    from microprediction import MicroCrawler
    crawler = MicroCrawler(write_key='YOUR WRITE KEY')
    crawler.run()


### Modifying the sample method
In this pattern we subclass MicroCrawler and override the method that takes lagged values and returns 225 guesses. 

    from microprediction import MicroCrawler
    import numpy as np 
    
    class MyCrawler(MicroCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def sample(self, lagged_values, lagged_times=None, **ignore ):
        """ Just a lame example of returning 225 values """
        x_std = np.nanstd(lagged_values)
        x_mean = np.nanmean(lagged_values)
        return sorted([ x*x_std+x_mean for x in np.random.randn(self.num_predictions) ])  

    mycrawler = MyCrawler(write_key='YOUR WRITE_KEY HERE')
    mycrawler.run()

Note self.num_predictions=225

### Other modifications
See [microprediction/crawler_examples_modification](https://github.com/microprediction/microprediction/tree/master/crawler_examples_modification). 


### Examples
See [predict-using-python-microcrawler-examples](https://microprediction.github.io/microprediction/predict-using-python-microcrawler-examples.html).

### Skating

See [predict-using-python-streamskater](https://microprediction.github.io/microprediction/streamskater.html).


### Where MicroCrawler sits in the hierarchy


         MicroReader
             |
         MicroWriter
             |
         MicroCrawler -----|
             |             |
         StreamSkater    


Thus if you want more control, you can [predict-using-python](https://microprediction.github.io/microprediction/predict-using-python.html) using MicroWriter. 

[Edit](https://github.com/microprediction/microprediction/blob/master/docs/predict-using-python-microcrawler.md) this page. 


![musk](/microprediction/assets/images/hardcore.jpeg)

