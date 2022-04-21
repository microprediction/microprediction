
### Stock and stock portfolio prediction examples
This directory provides examples of 
submitting distributional predictions of 45-minute ahead stock returns, and returns of portfolios of stocks. 

The stock streams:

- [stream=r_197](https://www.microprediction.org/stream_dashboard.html?stream=r_197)
 
The portfolio streams:

- [streams=p_334](https://www.microprediction.org/stream_dashboard.html?stream=p_34) 

The former correspond to tickers:
 
     from microprediction.live.xraytickers import XRAY_TICKERS 
     
or get directly in any language from [/live/xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) in any language. For
instance to avoid use of the microprediction client:

     from getjson import getjson      
     data = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json')

Similarly you can get [portfolios](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) with or without the client

    from microprediction.live.xrayportfolios import xray_portfolios
    w = xray_portfolios()
      
### Patterns using the precise library

Since the portfolio returns are determined from the stock returns, one pattern involves [estimating covariance](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_empirical_population_covariance.py) for all stocks using one of a hundred of
so methods provided in the precise package, then inferring the portfolio variances. Some adjustment for tails can be made. 

However it is also possible to directly forecast individual portfolios. See also [submission_examples_independent](https://github.com/microprediction/microprediction/tree/master/submission_examples_independent). 

