


## Bitcoin / Ethereum (c2 series)
See [An Empirical Article That Wasn't Immediately Stale](https://microprediction.medium.com/an-empirical-article-that-wasnt-immediately-stale-720abfb4678f) but note that it might be stale.  

### Scaled 5-minutely logarithmic changes 
Difference in change in log(price) multiplied by 1000x
* [c2_change_in_log_bitcoin](https://www.microprediction.org/stream_dashboard.html?stream=c2_change_in_log_bitcoin)
* [c2_change_in_log_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_change_in_log_ethereum)


### Changes in log of value of rebalanced portfolios 

* [c2_rebalanced_5](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_5) holding 5 percent bitcoin, 95 percent Ethereum
* [c2_rebalanced_55](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_55) holding 55 percent bitcoin, 45 percent Ethereum

and so forth, for increments of 5 percent. 

### Auxiliary streams possibly relevant to portfolio construction

The quadratic terms (changes in log prices multiplied)
* [c2_quadratic_full_ethereum_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_full_ethereum_ethereum)
* [c2_quadratic_full_bitcoin_bitcoin](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_full_bitcoin_bitcoin)
* [c2_quadratic_full_bitcoin_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_full_bitcoin_ethereum)
 
... also same thing focussed on lower moments (downside)
* [c2_quadratic_lower_ethereum_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_lower_ethereum_ethereum)
* [c2_quadratic_lower_bitcoin_bitcoin](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_lower_bitcoin_bitcoin)
* [c2_quadratic_lower_bitcoin_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_lower_bitcoin_ethereum)

... also same thing focussed on upper moments (upside)
* [c2_quadratic_upper_ethereum_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_upper_ethereum_ethereum)
* [c2_quadratic_upper_bitcoin_bitcoin](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_upper_bitcoin_bitcoin)
* [c2_quadratic_upper_bitcoin_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_quadratic_upper_bitcoin_ethereum)

### Crowd moments

Mean of all samples submitted for 15 minute ahead predictions of rebalanced portfolios
* [c2_rebalanced_65_mean](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_65_mean) Trimmed mean of predicted 15 minute ahead returns holding 65 percent bitcoin, 35 percent Ethereum
* [c2_rebalanced_5_mean](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_5_mean) Trimmed mean of predicted 15 minute ahead returns holding 5 percent bitcoin, 95 percent Ethereum
(and so on)

Also the standard deviations 
* [c2_rebalanced_5_std](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_5_std) Trimmed std of predicted 15 minute ahead returns holding 5 percent bitcoin, 95 percent Ethereum

### Some "info" porfolios

Info portfolio is created by looking at the crowd's predictions of the rebalanced portfolios and choosing one with the best info ratio 
* [c2_info_percent_bitcoin](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_percent_bitcoin) Recommended percentage bitcoin
* [c2_info_percent_ethereum](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_percent_ethereum) Recommended percentage ethereum 


Information ratio suggested portfolio returns, minus rebalanced
* [c2_info_return](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_return) Changes in log returns for "info" portfolio
1* [c2_info_minus_rebalanced_5](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_minus_rebalanced_5) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin, 95 percent Ethereum
* [c2_info_minus_rebalanced_25](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_minus_rebalanced_25) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 25 percent bitcoin, 75 percent Ethereum
* [c2_info_minus_rebalanced_35](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_minus_rebalanced_35) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 35 percent bitcoin, 65 percent Ethereum
* [c2_info_minus_rebalanced_45](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_minus_rebalanced_45) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 45 percent bitcoin, 95 percent Ethereum
* [c2_info_minus_rebalanced_55](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_minus_rebalanced_55) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 55 percent bitcoin, 95 percent Ethereum
* [c2_info_minus_rebalanced_65](https://www.microprediction.org/stream_dashboard.html?stream=c2_info_minus_rebalanced_65) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 65 percent bitcoin, 35 percent Ethereum
* [c2_info_minus_rebalanced_95](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_95) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 95 percent bitcoin, 5 percent Ethereum

Longer term profitability
* [c2_daily_info_minus_rebalanced_5](https://www.microprediction.org/stream_dashboard.html?stream=c2_daily_info_minus_rebalanced_5) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin, 95 percent Ethereum
* [c2_daily_info_minus_rebalanced_25](https://www.microprediction.org/stream_dashboard.html?stream=c2_daily_info_minus_rebalanced_25) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 25 percent bitcoin, 75 percent Ethereum
* [c2_daily_info_minus_rebalanced_35](https://www.microprediction.org/stream_dashboard.html?stream=c2_daily_info_minus_rebalanced_35) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 35 percent bitcoin, 65 percent Ethereum
* [c2_daily_info_minus_rebalanced_45](https://www.microprediction.org/stream_dashboard.html?stream=c2_daily_info_minus_rebalanced_45) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 45 percent bitcoin, 55 percent Ethereum
* [c2_daily_info_minus_rebalanced_55](https://www.microprediction.org/stream_dashboard.html?stream=c2_daily_info_minus_rebalanced_55) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 55 percent bitcoin, 45 percent Ethereum
* [c2_daily_info_minus_rebalanced_65](https://www.microprediction.org/stream_dashboard.html?stream=c2_daily_info_minus_rebalanced_65) Return of "info" strategy, less balanced portfolio with 5 percent bitcoin 65 percent bitcoin, 35 percent Ethereum
and so forth for all increments of 5 percent. 


## Related prizes

The raw aggregate regular leaderboards:
    - Emblossom Moth [https://api.microprediction.org/regular/e3b1055033076108b4279c473cde3a67](https://api.microprediction.org/regular/e3b1055033076108b4279c473cde3a67)
    - Fathon Gazelle [https://api.microprediction.org/regular/fa76039a2e11ed1f7d5d2cfec240455d](https://api.microprediction.org/regular/fa76039a2e11ed1f7d5d2cfec240455d)

See also this [notebook](https://github.com/microprediction/microprediction/blob/master/notebook_examples/List%20Current%20Prizes.ipynb) that shows how to list prizes on offer and related streams. 

## See also 

[Get Predictions](https://www.microprediction.com/get-predictions) guide at Microprediction.Com

## Literature
Lots of GARCH stuff. Examples. 

 - Modelling volatility of cryptocurrencies using Markov-Switching GARCH models. Caporale. Zekokh. [pdf](https://www.researchgate.net/publication/329866602_Modelling_volatility_of_cryptocurrencies_using_Markov-Switching_GARCH_models)

- Forecasting Bitcoin Risk Measures: A Robust Approach [pdf](https://www.researchgate.net/publication/325533373_Forecasting_Bitcoin_Risk_Measures_A_Robust_Approach)
