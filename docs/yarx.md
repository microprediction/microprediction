What are those [yarx](https://www.microprediction.org/stream_dashboard.html?stream=yarx_1n) streams? What about [xray](https://www.microprediction.org/stream_dashboard.html?stream=xray_182)? An approximate answer is the [code](https://github.com/microprediction/microprediction/blob/master/stream_examples_xray/xray.py) that generates them but actually that isn't quite the code that runs. There are prizes on offer for aggregate performance as you may have noticed on the [sub-leaderboards](https://www.microprediction.org/leaderboard.html). 


## Stock and protfolio streams

These are intended to provide "xray vision" into the joint behaviour of stocks. The portfolio [weights](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) are provided as JSON.  

 | Type           | Example stream                                                                            | Lookup       | Reverse lookup |
 |----------------|-------------------------------------------------------------------------------------------|---------------|---------------|
 | Stocks         | [stream=quick_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=quick_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=quick_xray_33](https://www.microprediction.org/stream_dashboard.html?stream=quick_xray_33) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |
 | Stocks         | [stream=middling_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=middling_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=middling_xray_33](https://www.microprediction.org/stream_dashboard.html?stream=middling_xray_33) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |
 | Stocks         | [stream=slow_yarx_googl](https://www.microprediction.org/stream_dashboard.html?stream=slow_yarx_googl)    | [xraytickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json) | [xraytickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickersreverse.json) |
 | Portfolios     | [stream=slow_xray_33](https://www.microprediction.org/stream_dashboard.html?stream=slow_xray_33) | [portfolios.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json) | |


Only 1 hour ahead predictions are considered relevant for prizes. 

### Volatility streams
There are derived feature streams

 | Type           | Example stream                                                                            | 
 |----------------|-------------------------------------------------------------------------------------------|
 | Vol            | [stream=vol_0_ma](https://www.microprediction.org/stream_dashboard.html?stream=vol_0_aapl)     |
 | Vol slope      | [stream=vol_1_ma](https://www.microprediction.org/stream_dashboard.html?stream=vol_1_aapl)     |
 | Vol convexity  | [stream=vol_2_ma](https://www.microprediction.org/stream_dashboard.html?stream=vol_2_aapl)     |
 

### Universe
Roughly, the top twenty stocks. 

    from microprediction.live.xraytickers import get_xray_tickers
    from microprediction.live.xrayportfolios import get_xray_portfolios
    symbols = get_xray_tickers()
    weights = get_xray_portfolios()
      

View [source](https://github.com/microprediction/microprediction/blob/master/docs/yarx.md)






