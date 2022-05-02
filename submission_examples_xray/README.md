
### Stock and stock portfolio streams

This directory provides examples of submitting distributional predictions for stock and portfolio price movements.

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
 


