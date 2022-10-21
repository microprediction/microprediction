What are those [yarx](https://www.microprediction.org/stream_dashboard.html?stream=yarx_1n) streams? What about [xray](https://www.microprediction.org/stream_dashboard.html?stream=xray_182)? The only truly accurate answer is the [code](https://github.com/microprediction/microprediction/blob/master/stream_examples_xray/xray.py) that generates them, but here we are in potentially stale doc land.

## Yarx equity streams

The honest answer is that the former represent a highly imperfect record of *some* changes in scaled log prices of stocks, and the latter are transparent linear combinations of those same changes published almost at the same time. 

This is, unfortunately, all subject to pretty severe limitations in the feed that drives them including delays and, shall we say, anomalies. Unfortunately, even 
if high quality live stock prices were ingested we would not have the rights to distribute them. But, that doesn't mean they aren't an important statistical exercise in the prediction of near-martingales and 
their curious distributional properties that have attracted considerable comment in the literature! 

These streams are sponsored by Hebdomad Leech by the way, whose full public sponsor code is

    6ebd03ad1eec6897b9414ff2a1b4501a

and you can use that to steer your crawler that way, shoud you wish. There are prizes on offer for aggregate performance across Hebdomad Leech's streams, as you may have noticed on the [sub-leaderboards](https://www.microprediction.org/leaderboard.html). 


## Xray portfolio streams

These are intended to provide "xray vision" into the joint behaviour of stocks. As noted these are portfolios, and indeed they are very loosely 


The portfolio [weights](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) are provided as JSON.  

 | Type           | Example stream                                                                            | Lookup       | Reverse lookup |
 |----------------|-------------------------------------------------------------------------------------------|---------------|---------------|
 | Stocks         | [stream=yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=xray_334](https://www.microprediction.org/stream_dashboard.html?stream=xray_334) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |

Only 1 hour ahead predictions are considered relevant, since at present the data sometimes falls back to 15 min delayed numbers (this may change).  

### Universe
Roughly, the universe is the set of IEX [eligible stocks](https://iextrading.com/trading/eligible-symbols/) for which balance sheet information is known and whose value of common stock was above $5 billion in Apr. Some conveniences are provided in the client if you don't wish to read JSON directly. 

    from microprediction.live.xraytickers import get_xray_tickers 
    from microprediction.live.xrayportfolios import get_xray_portfolios
    symbols = get_xray_tickers()
    weights = get_xray_portfolios()
      
      
### Examples of predicting portfolio returns directly

It is also possible to directly forecast individual portfolios using only their statistical properties. See [submission_examples_independent](https://github.com/microprediction/microprediction/tree/master/submission_examples_independent). 
      
### Examples of predicting portfolio returns from stock returns

COMING SOON. 

Should you wish to beat me to it, one pattern involves estimating covariance:

 - See [basic examples of covariance estimation](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_empirical_population_covariance.py) 
 - Swap out the covariance estimation for any method in the [precise](https://github.com/microprediction/precise) package. 
 








