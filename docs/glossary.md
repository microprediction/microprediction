## Glossary



| Term              | Intent                |
|-------------------|-----------------------|
| microprediction   | The act of making repeated predictions of the same thing frequently enough for autonomous assessment to be meaningful     |
| [crawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html)  | A python class for predicting multiple streams using a long-running single process |
|  [skating](https://microprediction.github.io/microprediction/predict-using-python-streamskater.html)              | Refers to the making of predictions in an online fashion. Applies to both time-series methods in the timemachines package, and also the StreamSkater crawler.       |
| cdf              | Cumulative distribution. In the microprediction context it usually refers to a cumulative distribution function implied by all the predictions contributed to a given forecast horizon. See any page such as [faang1&horizon=3555](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555).      |
| horizon | When predictions are made a horizon (also called delay) is specified. The ground truth is the first data point to be published
after the delay has elapsed |
| delay | See horizon. Delays are 70, 310, 910 or 3555 seconds.  |
| [publish](https://microprediction.github.io/microprediction/publish.html) | To send a scalar value to the microprediction system repeatedly, thereby creating a stream |
| [stream](https://microprediction.github.io/microprediction/publish.html) | A live time-series of scalar values that is subject to distributional prediction. See the [stream listing](https://www.microprediction.org/browse_streams.html)  |
| [polling](https://microprediction.github.io/microprediction/publish-using-python.html) | Refers to scheduled publishing, often using the [MicroPoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) class. |
| change function | Used in publishing changes of live quantities, or transforms of the same, using [MultiChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) or similar. |












                


-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)
 
