
### Stock and stock portfolio streams
This directory provides examples of 
submitting distributional predictions of 45-minute ahead stock returns, and returns of portfolios of stocks. Only 1 hour ahead predictions are considered relevant, since at present the data sometimes falls back to 15 min delayed numbers (this may change).  


 | Type           | Example                                                                                   | Meaning       |
 |----------------|-------------------------------------------------------------------------------------------|---------------|
 | Stocks         | [stream=r_197](https://www.microprediction.org/stream_dashboard.html?stream=r_197)        | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) |
 | Portfolios     | [stream=xray_334](https://www.microprediction.org/stream_dashboard.html?stream=xray_334) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) |

Some conveniences are provided in the client:

    from microprediction.live.xraytickers import XRAY_TICKERS 
    from microprediction.live.xrayportfolios import xray_portfolios
    w = xray_portfolios()
      
      
### Examples of predicting portfolio returns directly

It is also possible to directly forecast individual portfolios using only their statistical properties. See [submission_examples_independent](https://github.com/microprediction/microprediction/tree/master/submission_examples_independent). 
      
### Examples of predicting portfolio returns from stock returns

One pattern involves estimating covariance:

 - See [basic examples of covariance estimation](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_empirical_population_covariance.py) 
 - Swap out the covariance estimation for any method in the [precise](https://github.com/microprediction/precise) package. 
 


