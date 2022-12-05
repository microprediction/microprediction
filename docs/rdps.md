What are those [rdps](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp) streams? 


## Sector streams


 | Type           | Example stream                                                                            | Lookup       | Reverse lookup |
 |----------------|-------------------------------------------------------------------------------------------|---------------|---------------|
 | Sectors        | [stream=rdps_xlp](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp)    | [rdpstickers.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/rdpstickers.json) | [rdpstickersreverse.json](https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/rdpstickersreverse.json) |

Only 1 hour ahead predictions are considered relevant for prizes. 

For convenience:

    from microprediction.live.rdpstickers import get_rdps_tickers

## Sector copula z2-streams 

 | Type           | Example stream                                                                            | Purpose       |
 |----------------|-------------------------------------------------------------------------------------------|---------------|
 | z1-stream        | [z1~rdps_xlp~3555](https://www.microprediction.org/stream_dashboard.html?stream=z1~rdps_xlp~3555)    | Outliers |
 | z2-stream        | ['stream=z2~rdps_xlp~rdps_xlv~3555'](https://www.microprediction.org/stream_dashboard.html?stream=z2~rdps_xlp~rdps_xlv~3555)    | Bivariate |
 





### Examples of predicting sector streams directly:

Probably some in [submission_examples_independent](https://github.com/microprediction/microprediction/tree/master/submission_examples_independent) soon. 
      
      
View [source](https://github.com/microprediction/microprediction/blob/master/docs/rdps.md)
