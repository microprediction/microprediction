## Glossary



| Term              | Intent                |
|-------------------|-----------------------|
| microprediction   | The act of making repeated predictions of the same thing frequently enough for autonomous assessment to be meaningful     |
| [crawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html)  | A python class for predicting multiple streams using a long-running single process |
|  [skating](https://microprediction.github.io/microprediction/predict-using-python-streamskater.html)              | Refers to the making of predictions in an online fashion. Applies to both time-series methods in the timemachines package, and also the StreamSkater crawler.       |
| cdf              | Cumulative distribution. In the microprediction context it usually refers to a cumulative distribution function implied by all the predictions contributed to a given forecast horizon. See any page such as [faang1&horizon=3555](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555).      |
| daily prize | See [daily prize](https://www.microprediction.com/competitions/daily)    | 
| horizon | When predictions are made a horizon (also called delay) is specified. The ground truth is the first data point to be published
after the delay has elapsed |
| delay | See horizon. Delays are 70, 310, 910 or 3555 seconds.  |
| [publish](https://microprediction.github.io/microprediction/publish.html) | To send a scalar value to the microprediction system repeatedly, thereby creating a stream |
| [stream](https://microprediction.github.io/microprediction/publish.html) | A live time-series of scalar values that is subject to distributional prediction. See the [stream listing](https://www.microprediction.org/browse_streams.html)  |
| [polling](https://microprediction.github.io/microprediction/publish-using-python.html) | Refers to scheduled publishing, often using the [MicroPoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) class. |
| change function | Used in publishing changes of live quantities, or transforms of the same, using [MultiChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) or similar. |
| [zscores](https://microprediction.github.io/microprediction/zscores.html) | The distributional transform implied by (most of the) community predictions for pertaining to a particular horizon. |
| [zstreams](https://microprediction.github.io/microprediction/zscores.html) | Streams of [zscores](https://microprediction.github.io/microprediction/zscores.html)|
| [copulas](https://microprediction.github.io/microprediction/copulas.html) | In mathematics, a multivariate distribution with uniform margins. Here it usually refers to refers to z2~ or z3~ streams and their predictions. These are streams that are the result of merging two or three distributional transforms using a space-filling curve |
| space-filling curve | A map from the one dimension to two or three. See [copulas](https://microprediction.github.io/microprediction/copulas.html) |
| write key | A private unique identifier. See [writekeys](https://microprediction.github.io/microprediction/writekeys.html) |
| difficulty | The number of recognizable characters beginning a public key. See [writekeys](https://microprediction.github.io/microprediction/writekeys.html) |
| public key | The hash of a private key. See [writekeys](https://microprediction.github.io/microprediction/writekeys.html) |
| code | Synonym for public key. See [writekeys](https://microprediction.github.io/microprediction/writekeys.html) |
| memorable unique identifier | A synonym for private unique identifier. See [writekeys](https://microprediction.github.io/microprediction/writekeys.html) |
| burn | To create a new write key by trial and error. See [writekeys](https://microprediction.github.io/microprediction/writekeys.html) |
| [bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html) | When the balance associated with a write key falls below a threshold negative number | 
| [transfer](https://microprediction.github.io/microprediction/transfers.html) | To move balance from one write key to another |
| colab | A hosted Python notebook environment provided by Google. See [New_Key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) for example. |
| slack | A chat service. See [slack](https://microprediction.github.io/microprediction/slack.html) for invite. | 
| ground truth | A scalar value sent to microprediction, to serve as a target. See [publish](https://microprediction.github.io/microprediction/publish.html) | 
| submit | To send 225 scalars to microprediction. See [predict](https://microprediction.github.io/microprediction/predict.html) | 
| client | Usually refers to the microprediction [python package](https://github.com/microprediction/microprediction/tree/master/microprediction) | 
| leaderboard | Usually refers to [leaderboards](https://www.microprediction.org/leaderboard.html) shown at microprediction.org | 
| browser | Refers to [microprediction.org], a way for humans to see their performance and transactions |
| dashboard | Refers to [microprediction.org] after you paste a write key in. |
| lagged values | Refers to recent values of streams. See [predict-using-python](https://microprediction.github.io/microprediction/predict-using-python.html) for usage example. |
| z1~ streams | Streams prefixed by z1~. See [zscores](https://microprediction.github.io/microprediction/zscores.html) |
| z2~ streams | Streams prefixed by z2~. See [copulas](https://microprediction.github.io/microprediction/copulas.html) |
| z3~ streams | Streams prefixed by z3~. See [copulas](https://microprediction.github.io/microprediction/copulas.html) |














                


-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)
 
