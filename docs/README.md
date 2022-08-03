Let me explain briefly...

## 1. Free crowd-sourced live prediction via API ([>> PUBLISH >>](https://microprediction.github.io/microprediction/publish.html))

Take a moment to [browse the streams](https://www.microprediction.org/browse_streams.html) at microprediction.org. These are all created by people like you who publish scalar "ground truth" values one at a time, in order to initiate contests between prediction algorithms. The net result of these ongoing battles are beautiful community cumulative distribution functions accessed by API. An example is [this one](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) representing the 1-hour ahead distribution of changes to the logarithm of the price of META stock. You can create your own stream by modifying [create_a_stream.py](https://github.com/microprediction/microprediction/blob/master/hello_world/create_a_stream.py) and running it. 

See [publish](https://microprediction.
/microprediction/publish.html) for more advanced polling patterns, utilities, examples and more.   

## 2. Free benchmarking of algorithms ([>> PREDICT >>](https://microprediction.github.io/microprediction/predict.html))

On the other hand, perhaps you have an strong opinion about the distribution of future values of a die roll. You can modify the script called
[enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/hello_world/enter_die_contest_one_off.py) and run it. More likely you'll want to run a script that makes submissions on an ongoing basis, for something more interesting, and there are many utilities provided for that purpose, including the MicroCrawler class. You can paste your WRITE_KEY into the dashboard provided at [microprediction.org](https://www.microprediction.org/) to view the performance of your algorithm on diverse time-series. 

See [predict](https://microprediction.github.io/microprediction/predict.html) for more details and examples. 

### A few things to be aware of:

 - There is a daily cash prize for prediction of $125 USD. 
 - Interaction with the microprediction system is free and open to anyone, and merely requires a WRITE_KEY. Create yours by openning [New_Key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) in colab and letting it run for a few hours. Then paste your write key into the [www.microprediction.org](https://www.microprediction.org) dashboard. 
 - You probably want to join the [slack](https://microprediction.github.io/microprediction/slack.html). 
 - In the slack, I post a Google Meet invite for office hours: Fridays at noon eastern. Sometimes Tuesday nights too.  
 - By all means message [me](https://www.linkedin.com/in/petercotton/) on Linked-In, especially if the slack invite is stale. 
 - It is trivial to retrieve recent historical [data](https://microprediction.github.io/microprediction/data.html). 
  





