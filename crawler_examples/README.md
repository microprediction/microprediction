
# Guide to crawler examples

Incomplete list but should get you started. 

Need help? New video tutorials are available at https://www.microprediction.com/python-1 to help you
get started running crawlers at www.microprediction.com

## Timemachines package examples

Probably the easiest way to get a decent crawler going is by using the [timemachines](https://github.com/microprediction/timemachines) package. 

See [Bellehood Fox](https://github.com/microprediction/microprediction/blob/master/crawler_examples/bellehood_fox.py) for an example. 

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
As with ARIMA example above, this would also benefit from simple improvements but it works okay when
there is a lot of structure to be discovered. See [exactable fox](https://github.com/microprediction/microprediction/blob/master/crawler_examples/exactable_fox.py) or
[boatable clam](https://github.com/microprediction/microprediction/blob/master/crawler_examples/boatable_clam.py) for examples
of crawlers using ESN, and don't forget to pip install echochamber. 

## Ad-hoc empirical 

For example, [malaxable fox](https://github.com/microprediction/microprediction/blob/master/crawler_examples/malaxable_fox.py) eeks
out a living predicting the three-body system. 

## One-off z-predictions

As can be seen from examples like [Booze Mammal](https://github.com/microprediction/microprediction/blob/master/crawler_examples/booze_mammal.py) it is extremely
easy to make a living if z-streams are not accurate. That particular example always thinks the 
tails will be too thin, and I'll let you decide if that's a good idea or not.

## Default crawler

This may change from time to time. It is a recency-weighted bootstrappy sort of thing which as the
name suggests is trivial to run. See [dale leech](https://github.com/microprediction/microprediction/blob/master/crawler_examples/dale_leech.py) for
an example. Note that as with any crawler or MicroWriter you can instantiate with a difficulty argument and it will create
a new key on the fly. Thus using the default crawler is as easy as 

    from microprediction import MicroCrawler
    MicroCrawler(difficulty=11).run()
    
Don't discard the possibility that this may get you plenty of credits.  
   
