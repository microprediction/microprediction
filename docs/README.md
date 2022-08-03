A live exchange matching data to prediction algorithms. 

##  Free crowd-sourced prediction as a service ([>>THIS WAY>>](https://microprediction.github.io/get-predictions.html))

Take a moment to [browse the streams](https://www.microprediction.org/browse_streams.html) at microprediction.org. These are all created by people like you who publish scalar "ground truth" values one at a time, in order to initiate contests between prediction algorithms. The net result of these ongoing battles are beautiful community cumulative distribution functions. An example is [this one](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) representing the 1-hour ahead distribution of changes to the logarithm of the price of META stock. You can create your own stream by modifying [create_a_stream.py](https://github.com/microprediction/microprediction/blob/master/hello_world/create_a_stream.py) and running it. 

But see [get-predictions](https://microprediction.github.io/get-predictions.html) for polling utilities, patterns and examples. 

## Free leakage-free benchmarking of prediction algorithms ([>>THIS WAY>>](https://microprediction.github.io/make-predictions.html))

On the other hand, perhaps you have an strong opinion about the distribution of future values of a die roll. You can modify the script called
[enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/hello_world/enter_die_contest_one_off.py) and run it. Then, you paste your WRITE_KEY into the dashboard provided at [microprediction.org](https://www.microprediction.org/) to check on progress. More likely you'll want to run a script that makes submissions on an ongoing basis, and there are many utilities provided for that purpose including the MicroCrawler class. 

See [make-predictions](https://microprediction.github.io/make-predictions.html) for more details and examples. 

PS: Just want data? Links like [csv.microprediction.org/lagged?name=die.json](https://csv.microprediction.org/lagged?name=die.json) download the recent history of die rolls (say). But see [get-data](https://microprediction.github.io/get-data.html) for other ways, such as direct use of the API or Python client. 

## Before you start

 - Interaction with the microprediction system is free and open to anyone, and merely requires a WRITE_KEY. Create yours by openning [New_Key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) in colab and letting it run for a few hours. Then paste your write key into the [www.microprediction.org](https://www.microprediction.org) dashboard. 
 - You probably want to use the [slack](https://microprediction.github.io/slack.html) invitation (or message [me](https://www.linkedin.com/in/petercotton/) on Linked-In if this is stale).
 - In the slack, I post a Google Meet invite for open office hour: Fridays at noon eastern.   






