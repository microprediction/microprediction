## Skating

The [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) is intended to make it easy to use any time-series
point forecast method from the timemachines package. 

### StreamSkater pattern
Choose *f* from timemachines. 

     from microprediction.streamskater import StreamSkater
     from timemachines.skaters.simple.movingaverage import aggressive_ema_ensemble
     skater = StreamSkater(write_key='YOUR WRITE KEY', f=aggressive_ema_ensemble)
     skater.run()
     
See [timemachines](https://github.com/microprediction/timemachines) for an explanation of the behaviour expected of *f*. 


### Installing timemachines
See [timemachines/INSTALL](https://github.com/microprediction/timemachines/blob/main/INSTALL.md) instructions. 

### Where StreamSkater sits in the hierarchy

     MicroReader
         |
     MicroWriter
         |
     MicroCrawler
         | 
     StreamSkater 
     

Thus if you want more control, you can [predict-using-python-microcrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html).

-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)


