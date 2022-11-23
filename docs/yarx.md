What are those [yarx](https://www.microprediction.org/stream_dashboard.html?stream=yarx_1n) streams? What about [xray](https://www.microprediction.org/stream_dashboard.html?stream=xray_182)? An approximate answer is the [code](https://github.com/microprediction/microprediction/blob/master/stream_examples_xray/xray.py) that generates them but actually that isn't quite the code that runs.

## Yarx equity streams

There are prizes on offer for aggregate performance as you may have noticed on the [sub-leaderboards](https://www.microprediction.org/leaderboard.html). 


## Xray portfolio streams:

These are intended to provide "xray vision" into the joint behaviour of stocks. As noted these are portfolios, and indeed they are very loosely 


The portfolio [weights](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) are provided as JSON.  

 | Type           | Example stream                                                                            | Lookup       | Reverse lookup |
 |----------------|-------------------------------------------------------------------------------------------|---------------|---------------|
 | Stocks         | [stream=quick_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=quikc_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=quick_xray_33](https://www.microprediction.org/stream_dashboard.html?stream=quick_xray_33) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |


Only 1 hour ahead predictions are considered relevant for prizes. 

### Universe
Roughly, the universe is the set of IEX [eligible stocks](https://iextrading.com/trading/eligible-symbols/) for which balance sheet information is known and whose value of common stock was above a threshold. Some conveniences are provided in the client if you don't wish to read JSON directly. 

    from microprediction.live.xraytickers import get_xray_tickers
    from microprediction.live.xrayportfolios import get_xray_portfolios
    symbols = get_xray_tickers()
    weights = get_xray_portfolios()
      
### Stream names

    from microprediction.live.xraytickers import get_quick_yarx_stream_names
    from microprediction.live.xraytickers import get_middling_yarx_stream_names
    from microprediction.live.xraytickers import get_slow_yarx_stream_names
    
     
### Examples of predicting portfolio returns directly:

It is also possible to directly forecast individual portfolios using only their statistical properties. See [submission_examples_independent](https://github.com/microprediction/microprediction/tree/master/submission_examples_independent). 
      
### Examples of predicting portfolio returns from stock returns

COMING SOON. 

Should you wish to beat me to it, one pattern involves estimating covariance:

 - See [basic examples of covariance estimation](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_empirical_population_covariance.py) 
 - Swap out the covariance estimation for any method in the [precise](https://github.com/microprediction/precise) package. 
 








