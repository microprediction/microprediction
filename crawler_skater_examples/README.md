
## Timemachines skater-powered crawler examples

The timemachines package provides a simple interface for k-step ahead prediction of univariate (mostly) time-series. You might want to 
use the [timemachines](https://github.com/microprediction/timemachines) package in a MicroCrawler, or alternatively use the [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) class, which is intended to provide one way of
seamlessly integrating point estimates from timemachines into a crawler. 

Examples include:
 
 - [Bellehood Fox](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/bellehood_fox.py) moving average ensemble
 - [Datable Llama](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py) moving average ensemble
 - [Secable Llama](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/secable_llama.py) moving average ensemble
 - [Saccade Bee](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/saccade_bee.py) moving average ensemble
 - [Healthy Eel](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/healthy_eel.py) stacked moving averages
 - [Scotale Bee](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/scotale_bee.py) stacked moving averages
 - [Smeech Clam](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/smeech_clam.py) statsmodels.tsa (3,0,1)

As you can see from these examples:
- The timemachines forecasting packages allows you to use popular time series packages with one line of code, 
- The StreamSkater class in the microprediction package allows you to use any forecast method from the timemachines package, also with one line of code. 

      skater = StreamSkater(write_key=SACCADE_BEE, f=slow_aggressive_ema_ensemble, use_std=True, max_active=100)
      skater.run()

Thus these skaters are quite terse. You can view [Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_003.html) that give you some idea of whether a given method from the timemachines package will be any good at predicting live data at microprediction.org. 

### $ Equity streams $

See [Secable Llama](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/secable_llama.py) for an example of how to 
aim a skating crawler at equity market streams which have prize-money associated with them. 


 