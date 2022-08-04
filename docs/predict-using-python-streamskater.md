## Skating

The [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) is intended to make it easy to use any time-series
point forecast method from the timemachines package. You can simply use it as is, or sub-class. 

### Option 1. Use [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) without modification
Steps are:

1. Install timemachines carefully (see [instructions](https://github.com/microprediction/timemachines/blob/main/INSTALL.md))
2. Import a `time-series skater` *f*, perhaps after perusing the [Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/residual-k_001.html)
3. Instantiate a [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) using your WRITE_KEY
4. Call the run() method

A [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) example:


     from microprediction.streamskater import StreamSkater
     from timemachines.skaters.simple.movingaverage import aggressive_ema_ensemble
     skater = StreamSkater(write_key='YOUR WRITE KEY', f=aggressive_ema_ensemble)
     skater.run()

### Option 1a. Create a novel time-series skater *f*

You can also create a novel point forecast method *f* to feed to your StreamSkater. See the timemachines [README](https://github.com/microprediction/timemachines) for an explanation of
the behaviour expected of *f*. I'm sure the (ahem) author of that package would be *very* pleased
to receive more skater contributions. 


### Option 2. Modify [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py).sample_using_point_estimate()

1. Install timemachines carefully (see [instructions](https://github.com/microprediction/timemachines/blob/main/INSTALL.md))
2. Import a `time-series skater` *f*, perhaps after perusing the [Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/residual-k_001.html)
3. Sub-class [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) and modify the `sample_using_point_estimat` method
4. Instantiate using your WRITE_KEY ([remember](https://microprediction.github.io/microprediction/writekeys.html) ?)
5. Call the run() method

As a reminder,  this is the hierarchy we have covered. 

     MicroReader
         |
     MicroWriter
         |
     MicroCrawler
         | 
     StreamSkater 
     

By all means exert more control by backing up one step and [predict using MicroCrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html) instead.

-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)


