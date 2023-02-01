So you have a stock signal eh? Great. Prove it in realtime. 

### Criteria:

 - Does the signal apply to one or more of [these stocks](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) or to sectors ETFs? If not, sorry.  

### What to do: 

 - Create a program that produces 225 samples of the hour-ahead log price change. 
 - Presumably, these samples are nudged in the direction of your signal. 
 - Then see [prediction docs](https://microprediction.github.io/microprediction/predict.html)) for how to enter the fray. 

### That sounds hard
Then start here instead, and you'll get the joke quickly

  - Instantly participate using a default algorithm (see [setup](https://microprediction.github.io/microprediction/setup.html)).
  - Manually submit predictions by modifying
[enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/hello_world/enter_die_contest_one_off.py).
  - Then review the [prediction docs](https://microprediction.github.io/microprediction/predict.html) for submission patterns more likely to generalize.

## Brief explanation

The [streams](https://www.microprediction.org/browse_streams.html) at
microprediction.org are all created by people who repeatedly publish ground truths. Algorithms
poll these streams and the ongoing battles produce 
beautiful community cumulative distribution functions, such as the [CDF](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) representing the 1-hour ahead
forecasts of the logarithm of META price changes. There are [rewards](https://www.microprediction.com/competitions/daily) for good prediction determined daily. For a longer discussion see the [videos](https://github.com/microprediction/microprediction/blob/master/docs/videos.md) or the 
[book](https://microprediction.github.io/building_an_open_ai_network/) collateral.  


## Need more help? 
No, I'm not going to create some other bespoke mechanism to benchmark your signal. This one is perfectly fine IMHO. 

 - [Slack](https://microprediction.github.io/microprediction/slack.html) channel and Friday google [meet](https://microprediction.github.io/microprediction/meet.html).
 - [Glossary](https://microprediction.github.io/microprediction/glossary.html) and [summary](https://microprediction.github.io/microprediction/summary.html) of key API commands.
 - [Video](https://microprediction.github.io/microprediction/videos.html) tutorials
 - [Prizes](https://microprediction.github.io/microprediction/prizes.html). 
 - Join the [slack](https://microprediction.github.io/microprediction/slack.html) or Friday [meet](https://microprediction.github.io/microprediction/meet.html) so we can help you get started.
  
  
## More info on the equity prediction contests
Want to win the daily prize?

 - [yarx](https://microprediction.github.io/microprediction/yarx.html) ... stock changes and features
 - [rdps](https://microprediction.github.io/microprediction/rdps.html) ... sector changes and copulas
  
What are you waiting for? 
  
-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html) 

View [source](https://github.com/microprediction/microprediction/blob/master/docs/signals.md) or as [web page](https://microprediction.github.io/microprediction/signals)


![where_did_my_money_go](/microprediction/assets/images/where_did_my_money_go.png)






