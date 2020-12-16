
# Guide to crawler examples

Incomplete list but should get you started. 

## Filtering examples

It probably
goes without saying that this kind of model is intended for noisy data. You'll want to familiarize
 yourself with FitCrawler, for instance by reading the operation of [SequentialStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/sequentialcrawler.py) and how
 this uses [DistMachine](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/distmachine.py). There 
 is a
[video introduction to FitCrawler](https://www.microprediction.com/fitcrawler).  

### ExpNorm examples

These use the [ExpNormDist](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/expnormdist.py) which generalizes the
Kalman filter. Measurement noise is a mixture of normal and exponential, and the gain is somewhat
arbitrarily chosen.  

![](https://i.imgur.com/PpWIhlx.png)

[Floatable Bee](https://github.com/microprediction/microprediction/blob/master/crawler_examples/floatable_bee.py)
uses only on-the-fly fitting only, and does not try to use stored parameters. It is set to ony run for 35 streams.
This consumes around 20,000 cpu seconds per month. 

Other crawlers such as [Yex Cheetah](https://github.com/microprediction/microprediction/blob/master/crawler_examples/yex_cheetah.py) take advantage 
of [stored parameter]('https://raw.githubusercontent.com/microprediction/offline/main/modelfits/expnorm') that are
updated periodically by a separate process (using Github actions). Images such as [this one](https://github.com/microprediction/offline/blob/main/modelfits/expnorm/z1~electricity-lbmp-nyiso-north~70.png) 
from the fitting are also stored there, so you can judge for yourself how well the filter is behaving. 

### t-Digest 

[Thallodal Cat](https://github.com/microprediction/microprediction/blob/master/crawler_examples/thallodal_cat.py) is a different
 species but it is also a [SequentialStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/sequentialcrawler.py). The 
  difference is that it uses a simple [DigestDist](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/digestdist.py) in 
  place of a parametric model. 
  
### Skew-Normal 

A more speculative crawler, also intended for noisy data, uses [SkewDist](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/skewdist.py). This attempts
to maintain a Moment based approximate skew normal distribution machine based on a [stackoverflow answer](https://stackoverflow.com/questions/49801071/how-can-i-use-skewnorm-to-produce-a-distribution-with-the-specified-skew) I 
stumbled upon and cleaned up. There are some limitations to the moment fitting procedure, but sometimes
this works okay regardless. See for example [Mesole Mammal](https://github.com/microprediction/microprediction/blob/master/crawler_examples/mesole_mammal.py). 

## ARIMA

See [Soshed Boa](https://github.com/microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py) for an example of using statsmodels.tsa.ar_model with automated order selection. This is a pretty
bare-bones crawler at time of writing and could benefit from simple improvements, such as projecting
onto discrete values when the time series is obviously quantized (see utilities in [cdfvalues](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/cdfvalues.py)). 

## Echo state machines

See the [echochamber](https://github.com/microprediction/echochamber) package. As you can see from 
the [crawler code](https://github.com/microprediction/echochamber/blob/master/echochamber/crawler.py), the ESN is so fast to fit that it simply does it on the fly. 
As with ARIMA example above, this would also benefit from simple improvements. 