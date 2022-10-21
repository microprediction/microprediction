## FitCrawler

The [FitCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/fitcrawler.py) is derived from
[SequentialStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/sequentialcrawler.py) and the intent is that
the subclasser will modify it not by subclassing necessarily, but by providing at time of construction a means of sequentially fitting a distribution. 

     MicroCrawler
         | 
     SequentialStreamCrawler
         |
     FitCrawler

Now [SequentialStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/sequentialcrawler.py) is useful if the 
process is well approximated by independent increments, or when each prediction is essentially a prediction of a single increment. Then in addition,
[FitCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/fitcrawler.py) helps out if you expect to be reading parameters from
an offline fit, or at least trying to do so. 

### Prerequisite knowledge:distribution machines

To use FitCrawler effectively one must understand the [FitDist](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/fitdist.py) class.
This is intended to abstract the notion of a walking, talking cumulative distribution function that informs itself as it receives data one point 
at a time. A DistMachine is characterized by:

    def update(self, value=None, dt=None, **kwargs):
        # Incorporate new value, time passing, or both
        # Typically will update the state but not params
        raise NotImplementedError

    def inv_cdf(self, p: float) -> float:
        # Something like StatsConventions.norminv(p)
        raise NotImplementedError

A [LossDist](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/fitdist.py) is a DistMachine that also has the notion
of a loss function (which might be log-likelihood). It's contribution is wrapping up the ability to run itself over past data and report aggregate scores that can
be used for estimation. The FitDist provides some additional functionality over a LossMachine, because it provides a default way of fitting the distribution (or
we might say hyper-fitting it, by default using the HyperOpt package). 

An example of a non-trivial FitDist is provided by [expnormdist](https://github.com/microprediction/microprediction/blob/master/microprediction/univariate/expnormdist.py) which, as the name 
suggests, attempts to maintain an exponential normal distribution (actually two of them). 

To summarize, (and see [/univariate](https://github.com/microprediction/microprediction/tree/master/microprediction/univariate)):

    DistMachine   
        |
    LossMachine
        | 
    FitDist


## SequentialStreamCrawler

With that out of the way, let us return to [SequentialStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/sequentialcrawler.py) and
observe that by default it provides remotely sensible update_state and sample_using_state methods. That's why SequentialStreamCrawler can be used
without subclassing. Instead you change the default distribution machine that is passed to it at construction time (the default is the t-Digest, which you
can read about in the article [Live Online Distribution Estimation Using t-Digests](https://www.linkedin.com/pulse/live-online-distribution-estimation-using-t-digests-peter-cotton-phd/). 

### FitCrawler

Backing up one more step, we can now say that you'd want to use FitCrawler if the following is true:

  1. You are okay modeling the process as independent increments (or you care to override the default sample_using_state method)
  2. You like the idea of fitting parameters offline, and reading them from a url

If all of this sounds complicated, the usage isn't. Indeed you can see from [comal_cheetah](https://github.com/microprediction/microprediction/blob/master/crawler_examples/comal_cheetah.py) that
FitCrawler has taken away all of the trouble one would normally go to. All Comal Cheetah does is pick a distribution machine, instantiate itself with some parameters including
a url where stored parameters are expected to be found, and runs. The model parameters are to be found [here](https://github.com/microprediction/offline/tree/main/modelfits/expnorm). 

### Video help

There is a [video](https://www.microprediction.com/fitcrawler) about the use of FitCrawler. 


     

-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)


