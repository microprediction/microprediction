# Submitting stock or volatility signals

So you have a stock signal eh? Great. Does the signal apply to one or more of [these stocks](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) or to sectors ETFs? Does it help predict either the mean *or the distribution* of log stock prices? Wonderful, unlike all those other people you spammed on Linked-In I am actually willing to form an opinion on your work and I'm even willing to help you win the [prizes](https://microprediction.github.io/microprediction/prizes.html). I do not, however, give a damn how your system performed in the past.     

### The Microprediction benchmarking platform

The [streams](https://www.microprediction.org/browse_streams.html) at
microprediction.org are all created by people who repeatedly publish ground truths. Some are stock market streams. Others electricity, and so on.

Algorithms hosted and run by anyone can poll these streams and send predictions to the server. The ongoing battles produce 
beautiful community cumulative distribution functions, such as the [CDF](https://www.microprediction.org/stream_dashboard.html?stream=quick_yarx_goog&horizon=3555) representing the 1-hour ahead
forecasts of the logarithm of Google price changes. See these doc pages:

 - [yarx](https://microprediction.github.io/microprediction/yarx.html) ... stock changes and features
 - [rdps](https://microprediction.github.io/microprediction/rdps.html) ... sector changes and copulas

There are [rewards](https://www.microprediction.com/competitions/daily) for good prediction determined daily. 

### How to use this platform to prove that you have a useful signal
The platform simultaneously benchmarks both distributional and directional signals. 

 - Create a program that produces 225 samples of the hour-ahead log price change. 
 - Presumably, these samples are nudged in the direction of your directional signal or dilated according to your volatility signal. You can approximate a long or short position, if you wish, or any options payoff, more or less.   
 - Then see [prediction docs](https://microprediction.github.io/microprediction/predict.html) for how to programmatically send them. 


### Dispensing with lame excuses:

  1. If your signal is "long-term" use that thing called [division](https://en.wikipedia.org/wiki/Division_(mathematics)) or, if necessary taking a square root. And yes, to reiterate, one can easily create approximate long or short positions in a continuous generalization of a parimutuel. Just multiply a reasonable guess of the market distribution Q(x) by your desired payoff if you can't devise a more precise way. And you need only submit once, since your submission will carry over for a day or week or month if you don't cancel it.  

  2. If you don't grok the mechanics, then first just instantly participate using a default algorithm (see [setup](https://microprediction.github.io/microprediction/setup.html)). Or even manually submit predictions by modifying
[enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/hello_world/enter_die_contest_one_off.py). Then circle back and review the [prediction docs](https://microprediction.github.io/microprediction/predict.html) for submission patterns more likely to generalize.

 3. If you don't understand the game or its strategy, read about it [here](https://www.microprediction.com/blog/intro) or read the [prediction docs](https://microprediction.github.io/microprediction/predict.html). 


If you are smart enough to beat the market you are smart enough to grok a simple game, and API or Python client. No, I'm not going to create some other bespoke mechanism to benchmark your signal or do any work beyond what I've already done. For example, if you have a strategy that profits with longs and shorts and it can't also win this game (with approximate longs and shorts) then your strategy might be among the most overfitted in history. So I will not accept the response that "your strategy cannot be tested on this platform". That is clearly a nonsense position. 

But I offer the following: 

 - [Slack](https://microprediction.github.io/microprediction/slack.html) channel and Friday google [meet](https://microprediction.github.io/microprediction/meet.html).
 - [Glossary](https://microprediction.github.io/microprediction/glossary.html) and [summary](https://microprediction.github.io/microprediction/summary.html) of key API commands.
 - [Video](https://microprediction.github.io/microprediction/videos.html) tutorials
 - Join the [slack](https://microprediction.github.io/microprediction/slack.html) or Friday [meet](https://microprediction.github.io/microprediction/meet.html) so we can help you get started.
  
  
-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html) 

View [source](https://github.com/microprediction/microprediction/blob/master/docs/signals.md) or as [web page](https://microprediction.github.io/microprediction/signals)


![where_did_my_money_go](/microprediction/assets/images/where_did_my_money_go.png)

[Acknowledgement](https://xkcd.com/1570/)




