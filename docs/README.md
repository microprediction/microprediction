The two sides of this free open API and Python client are:

## 1. Crowd-sourced live prediction ([>>PUBLISH >>](https://microprediction.github.io/microprediction/publish.html))

Take a moment to [browse the streams](https://www.microprediction.org/browse_streams.html) at microprediction.org. These are all created by people like you who publish scalar "ground truth" values one at a time, in order to initiate contests between prediction algorithms. The net result of these ongoing battles are beautiful community cumulative distribution functions accessed by API. An example is [this one](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) representing the 1-hour ahead distribution of changes to the logarithm of the price of META stock. You can create your own stream by modifying [create_a_stream.py](https://github.com/microprediction/microprediction/blob/master/hello_world/create_a_stream.py) and running it. 

See [publish](https://microprediction.github.io/publish.html) for more advanced polling patterns, utilities, examples and more.   

## 2. Benchmarking of algorithms ([>> PREDICT >>](https://microprediction.github.io/microprediction/predict.html))

On the other hand, perhaps you have an strong opinion about the distribution of future values of a die roll. You can modify the script called
[enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/hello_world/enter_die_contest_one_off.py) and run it. More likely you'll want to run a script that makes submissions on an ongoing basis, for something more interesting, and there are many utilities provided for that purpose, including the MicroCrawler class. You can paste your WRITE_KEY into the dashboard provided at [microprediction.org](https://www.microprediction.org/) to view the performance of your algorithm on diverse time-series. 

See [predict](https://microprediction.github.io/microprediction/predict.html) for more details and examples. 

## Highlights

 - Daily $125 [prize](https://www.microprediction.com/competitions/daily).  
 - Use a [colab notebook](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) to get your WRITE_KEY. 
 - Join the [slack](https://microprediction.github.io/microprediction/slack.html). 
 - Office hours: Fridays at noon eastern. Sometimes Tuesday nights.  
 - Free [data](https://microprediction.github.io/microprediction/data.html). 
  






