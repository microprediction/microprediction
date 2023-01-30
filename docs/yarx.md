What are those [yarx](https://www.microprediction.org/stream_dashboard.html?stream=yarx_1n) streams? What about [xray](https://www.microprediction.org/stream_dashboard.html?stream=xray_182)? An approximate answer is the [code](https://github.com/microprediction/microprediction/blob/master/stream_examples_xray/xray.py) that generates them but actually that isn't quite the code that runs. There are prizes on offer for aggregate performance as you may have noticed on the [sub-leaderboards](https://www.microprediction.org/leaderboard.html). 


## Stock and protfolio streams

These are intended to provide "xray vision" into the joint behaviour of stocks. The portfolio [weights](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) are provided as JSON.  

 | Type           | Example stream                                                                            | Lookup       | Reverse lookup |
 |----------------|-------------------------------------------------------------------------------------------|---------------|---------------|
 | Stocks         | [stream=quick_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=quick_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=quick_xray_3](https://www.microprediction.org/stream_dashboard.html?stream=quick_xray_3) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |
 | Stocks         | [stream=middling_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=middling_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=middling_xray_3](https://www.microprediction.org/stream_dashboard.html?stream=middling_xray_3) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |
 | Stocks         | [stream=slow_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=slow_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=slow_xray_3](https://www.microprediction.org/stream_dashboard.html?stream=slow_xray_3) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |
 
Only 1 hour ahead predictions are considered relevant for prizes. 

### Volatility streams
There are derived feature streams

 | Type           | Example stream                                                                            | Meaning        |
 |----------------|-------------------------------------------------------------------------------------------|----------------
 | Vol            | [stream=yarx_vlty_0_aapl](https://www.microprediction.org/stream_dashboard.html?stream=yarx_vlty_0_aapl)     | Scaled log of middling_yarx_appl predictions interquartile range |
 | Vol slope      | [stream=yarx_vlty_1_aapl](https://www.microprediction.org/stream_dashboard.html?stream=yarx_vlty_1_aapl)     | Difference between scaled log quick and log slow inter-quartile ranges |
 | Vol convexity  | [stream=yarx_vlty_2_aapl](https://www.microprediction.org/stream_dashboard.html?stream=yarx_vlty_2_aapl)     | Similar, but the convexity | 
 
### Exogenous data streams
Some exogenous features are being added that tick infrequently. They may be useful in your models, however. 

 | Type           | Example stream                                                                            | Meaning        |
 |----------------|-------------------------------------------------------------------------------------------|----------------
 | Vol            | [stream=yarx_exog_0_aapl](https://www.microprediction.org/stream_dashboard.html?stream=yarx_exog_0_aapl)     | Vol feature |

(ignore any exog_yarx streams they are deprecated)


### Universe
Roughly, the top 100 stocks. 

    from microprediction.live.xraytickers import get_xray_tickers
    from microprediction.live.xrayportfolios import get_xray_portfolios
    symbols = get_xray_tickers()
    weights = get_xray_portfolios()
      

View [source](https://github.com/microprediction/microprediction/blob/master/docs/yarx.md)






