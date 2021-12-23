
# microprediction [![Downloads](https://static.pepy.tech/personalized-badge/microprediction?period=total&units=international_system&left_color=green&right_color=grey&left_text=Downloads)](https://pepy.tech/project/microprediction) ![tests](https://github.com/microprediction/microprediction/workflows/tests/badge.svg) ![deploy](https://github.com/microprediction/microprediction/workflows/deploy/badge.svg)

## Who is this microprediction user?

Looking for [microprediction](https://github.com/microprediction/microprediction/tree/master/microprediction)? I guess Github made this a "user home page". Well hi, this is my [dog](https://i.imgur.com/2E3pskp.jpg). This is my [blog](https://www.microprediction.com/blog).  I'm the author of these packages:
- [HumpDay](https://github.com/microprediction/humpday) - Derivative-free optimizers in canonical form, with [Elo ratings](https://microprediction.github.io/optimizer-elo-ratings/html_leaderboards/overall.html) 
- [FirstDown](https://github.com/microprediction/firstdown) - The repo that might ruin the great game of football.  
- [MUID](https://github.com/microprediction/muid) - Memorable Unique Identifiers. The only thing I'll be remembered for. 
- [Embarrassingly](https://github.com/microprediction/embarrassingly) - A speculative approach to robust optimization that sends impure objective functions to optimizers.
- [Winning](https://github.com/microprediction/winning) - A recently published fast algorithm for inferring relative ability from win probability (stable). 
- [Pandemic](https://github.com/microprediction/pandemic) - Ornstein-Uhlenbeck epidemic simulation (related [paper](https://arxiv.org/abs/2005.10311))
- [m6](https://github.com/microprediction/m6) - Some utilities for the M6 Forecasting competition (fast numerical rank probabilities without Monte Carlo)

and a few others. But I suspect you are here for one of these two:

- [TimeMachines](https://github.com/microprediction/timemachines) - Autonomous time-series prediction algorithms in simple functional form, also with [Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_003.html)
- [Microprediction](https://github.com/microprediction/microprediction) - The client for [api.microprediction.org](https://api.microprediction.org/) making it easier to either publish live data one point at a time so it will be predicted, or submit predictions for existing streams. 
 
So while both are aimed at time-series, and mostly autonomous univariate prediction of the same, the [TimeMachines](https://github.com/microprediction/timemachines) package is traditional open-source software for point-estimates and confidence, whereas the [Microprediction](https://github.com/microprediction/microprediction) client offers "algorithm-crowd-based" distributional prediction. 

## What's this microprediction client? 
If you don't know about the live algorithm frenzy at [microprediction.org](https://www.microprediction.org/) then an extremely simple way to grok it is to open this [notebook](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/first_submission.ipynb) and run it. This will create an identity for you and enter your algorithm in an ongoing contest to predict the next roll of a die. 

The [client](https://github.com/microprediction/microprediction) hits the [microprediction api](http://api.microprediction.org/), enabling turnkey, *repeated short term predictions* of anything, for any purpose, for anyone, at any time, as follows: 

 0. You create an identity (the package's *new_key* function). 
 1. You create a stream one scalar data point at a time. (*set* method on MicroWriter)
 2. Algorithms watch it and submit 225 guesses of the value of future data values.  (*submit* method on MicroWriter)
 3. You retrieve predictions at any time. (*get_predictions* method on MicroReader or get_own_predictions on MicroWriter)

Thus this is a probabilistic exchange, of sorts. 

## I just wanna see examples
Fair enough. [README_EXAMPLES.md](https://github.com/microprediction/microprediction/blob/master/README_EXAMPLES.md)

## What's the difference between [Microprediction.Com](https://www.microprediction.com/) and [Microprediction.org](https://www.microprediction.org/)?

The former is an educational site for the latter. The [blog](https://www.microprediction.com/blog) is a way to create content to help spread the idea of open, collective, community prediction.  

## Slack / Google Meets are recommended

Most people looking to contribute to this open initiative (and win beer money) join the [microprediction slack](https://join.slack.com/t/microprediction/shared_invite/zt-10ad1yiec-Jgsjkit~~dwNnpvRzyBTaQ). If that invite fails there might be one in the [knowledge center](https://www.microprediction.com/knowledge-center) that hasn't expired. 

Many contributors also stop by our twice weekly virtual chats which you are welcoem to. See the [knowledge center](https://www.microprediction.com/knowledge-center) for Google Meet details. Tue 8pm and Fri noon EST.  

## Microprediction bookmarks

**Data**: [stream list](https://www.microprediction.org/browse_streams.html) | [stream explanations](https://www.microprediction.com/blog/livedata) | [csv](https://www.microprediction.org/features.html) **Client**: [client](https://github.com/microprediction/microprediction) | [reader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py) | [writer](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) | [crawler](https://github.com/microprediction/microprediction/blob/master/microprediction/crawler.py) | [crawler examples](https://github.com/microprediction/microprediction/tree/master/crawler_examples) | [notebook examples](https://github.com/microprediction/microprediction/tree/master/notebook_examples)
**Resources**: [popular timeseries packages](https://www.microprediction.com/blog/popular-timeseries-packages) |
[knowledge center](https://www.microprediction.com/knowledge-center) | [faq](https://www.microprediction.com/faq) |
[linked-in](https://www.linkedin.com/company/65109690) |
[microprediction.org (dashboard)](https://www.microprediction.org) | [microprediction.com (resources)](https://www.microprediction.com) |
[what](https://www.microprediction.com/what) | [blog](https://www.microprediction.com/blog) | [contact](https://www.microprediction.com/contact-us) |
[competitions](https://www.microprediction.com/competitions) |
[make-predictions](https://www.microprediction.com/make-predictions) |
[get-predictions](https://www.microprediction.com/get-predictions) |
[applications](https://www.microprediction.com/welcome-3) | [collective epidemiology](https://www.swarmprediction.com/about.html) 
**Video tutorials** : [1: non-registration](https://www.microprediction.com/python-1) | [2: first crawler](https://www.microprediction.com/python-2) |[3: retrieving historical data](https://www.microprediction.com/python-3) | [4: creating a data stream](https://www.microprediction.com/python-4) | [5: modifying your crawler's algorithm](https://www.microprediction.com/python-5) | 
[6: modifying crawler navigation](https://www.microprediction.com/python-6) 
**Colab notebooks**
[creating a new key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) |
[listing current prizes](https://github.com/microprediction/microprediction/blob/master/notebook_examples/List%20Current%20Prizes.ipynb) |
[submitting a prediction](https://github.com/microprediction/microprediction/blob/master/notebook_examples/Python_Module_1_First_Submission.ipynb) | 
[choosing streams](https://github.com/microprediction/microprediction/blob/master/notebook_examples/Crawler_choosing_streams.ipynb) |
[retrieving historical data](https://github.com/microprediction/microprediction/blob/master/notebook_examples/Python_Module_3_Getting_History.ipynb)
**Related** [humpday](https://github.com/microprediction/humpday) | [timemachines](https://github.com/microprediction/timemachines) | [timemachines-testing](https://github.com/microprediction/timemachines-testing) | [microconventions](https://github.com/microprediction/microconventions) | [muid](https://github.com/microprediction/muid) | [causality graphs](https://github.com/microprediction/microactors-causality/tree/main/gallery) | [embarrassingly](https://github.com/microprediction/embarrassingly) | [key maker](https://github.com/microprediction/keymaker) | [real data](https://github.com/microprediction/realdata)| [chess ratings prediction](https://github.com/microprediction/chess) 
**Eye candy** [copula plots](https://github.com/microprediction/microactors-plots/tree/main/gallery) | [causality plots](https://github.com/microprediction/microactors-causality/tree/main/gallery) | [electricity case study](https://www.linkedin.com/posts/rusty-conover-ba5a6_predicting-nys-electricity-using-machine-activity-6750837765761503233-vYFu) 

Probably best to start in the [knowledge center](https://www.microprediction.com/knowledge-center) and remember [Dorothy, You're Not in Kaggle Anymore](https://www.linkedin.com/pulse/dorothy-youre-kaggle-anymore-peter-cotton-phd/). 

## Open, turnkey prediction.  

Here's how it operates. 
- You publish live data repeatedly, [like this](https://github.com/microprediction/microprediction/blob/master/feed_examples_live/traffic_live.py) say, and it
 creates a stream like [this one](https://www.microprediction.org/stream_dashboard.html?stream=electricity-load-nyiso-overall).
- As soon as you do, algorithm "crawlers" like [this guy](https://github.com/microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py) compete to make distributional predictions of
your data feed 1 min ahead, 5 min ahead, 15 min ahead and 1 hr ahead. 

In this way you can:
 - Get live prediction of public data for free (yes it really is an [api](http://api.microprediction.org/) that predicts anything!)
 - See which R, Julia and Python time series approaches seem to work best, saving you from
  trying out [hundreds of packages](https://www.microprediction.com/blog/popular-timeseries-packages) from PyPI and github of uncertain quality. 
  

## Cite
See [CITE.md](https://github.com/microprediction/microprediction/blob/master/CITE.md)

## FAQ:
- Moved to [FAQ](https://www.microprediction.com/faq) 

## Video tutorials
See the [Knowledge Center](https://www.microprediction.com/knowledge-center)

## The longer README.md for the microprediction client
[README_LONGER.md](https://github.com/microprediction/microprediction/blob/master/README_LONGER.md)
