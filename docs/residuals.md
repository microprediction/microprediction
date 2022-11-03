
# How to use microprediction for ongoing model residual analysis
Steps
   
   1. Publish model residuals (see [publishing docs](https://microprediction.github.io/microprediction/publish.html))

   2. (optional) Submit a simple prediction, such as N(0,1), or whatever you believe your model residuals to be (see [prediction docs](https://microprediction.github.io/microprediction/predict.html)). 

That's all. Later, you can see how well the null hypothesis is performing on the leaderboards that will be created for your stream. If you consider model residuals proprietary, then by all means transform them first. And check with your compliance department. 


## Brief explanation

The [streams](https://www.microprediction.org/browse_streams.html) at
microprediction.org are all created by people who repeatedly publish ground truths. Algorithms
poll these streams and the ongoing battles produce 
beautiful community cumulative distribution functions, such as the [CDF](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) representing the 1-hour ahead
forecasts of the logarithm of META price changes. There are [rewards](https://www.microprediction.com/competitions/daily) for good prediction determined daily. For a longer discussion see the [videos](https://github.com/microprediction/microprediction/blob/master/docs/videos.md) or the 
[book collateral](https://microprediction.github.io/building_an_open_ai_network/).  

-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html) 

View [source](https://github.com/microprediction/microprediction/blob/master/docs/README.md)


![skipped](/microprediction/assets/images/skipped_statistics.png)
