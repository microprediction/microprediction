What are those [rdps](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp) streams? 


## Sector streams


 | Type           | Example stream                                                                            | Lookup       | Reverse lookup |
 |----------------|-------------------------------------------------------------------------------------------|---------------|---------------|
 | Sectors        | [stream=rdps_xlp](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp)    | [rdpstickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/rdpstickers.json) | [rdpstickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/rdpstickersreverse.json) |

Only 1 hour ahead predictions are considered relevant for prizes. 

### Exogenous data streams
Some exogenous features are being added that tick infrequently. They may be useful in your models, however. 

 | Type           | Example stream                                                                            | Meaning        |
 |----------------|-------------------------------------------------------------------------------------------|----------------
 | Vol            | [stream=rdps_exog_0_aapl](https://www.microprediction.org/stream_dashboard.html?stream=yarx_exog_0_aapl)     | Vol feature |

(ignore any exog_rdps or exog_0_rdps streams as they are deprecated)


## Sector copula z2-streams 
Reported bivariate relationships

 | Type           | Example stream                                                                            | Explanation       |
 |----------------|-------------------------------------------------------------------------------------------|---------------|
 | z1-stream        | [z1\~rdps_xlp\~3555](https://www.microprediction.org/stream_dashboard.html?stream=z1~rdps_xlp~3555)    | [Z-scores](https://microprediction.github.io/microprediction/zscores.html)  |
 | z2-stream        | [stream=z2\~rdps_xlp\~rdps_xlv\~3555](https://www.microprediction.org/stream_dashboard.html?stream=z2~rdps_xlp~rdps_xlv~3555)    | [copulas](https://microprediction.github.io/microprediction/copulas.html) |
 

### Client helper functions
For convenience:

    from microprediction.live.rdpstickers import get_rdps_tickers

Might be more [here](https://github.com/microprediction/microprediction/tree/master/microprediction/live). 

### Examples of predicting sector streams directly:

Probably some in [submission_examples_independent](https://github.com/microprediction/microprediction/tree/master/submission_examples_independent) soon. 
      
      
View [source](https://github.com/microprediction/microprediction/blob/master/docs/rdps.md)
