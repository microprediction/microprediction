### 1. Free distributional prediction

Take a moment to [browse the streams](https://www.microprediction.org/browse_streams.html) at microprediction.org. These are all created by people like you who publish scalar "ground truth" values one at a time, in order to initiate contests between prediction algorithms. The net result of these ongoing battles are beautiful community cumulative distribution functions like [this one](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) for the 1-hour ahead distriubtion of changes to the logarithm of the price of META stock. You can create your own stream by modifying [create_a_stream.py](https://github.com/microprediction/microprediction/blob/master/hello_world/create_a_stream.py) and running it. 

See [get-predictions](https://microprediction.github.io/dotcom/get-predictions.html) for more details and examples. 

### 2. Free benchmarking of algorithms

On the other hand, perhaps you have an strong opinion about the distribution of future values of a die roll. You can modify the script called
[enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/hello_world/enter_die_contest_one_off.py) and run it. Then, you paste your WRITE_KEY into the dashboard provided at [microprediction.org](https://www.microprediction.org/) to check on progress. More likely you'll want to run a script that makes submissions on an ongoing basis, and there are many utilities provided for that purpose including the MicroCrawler class. 

See [make-predictions](https://microprediction.github.io/dotcom/make-predictions.html).  

### 3. Free data for time-series research

You can download the recent history of die rolls from [csv.microprediction.org/lagged?name=die.json](https://csv.microprediction.org/lagged?name=die.json), although other API or Python client use may be simpler. 

See [get-data](https://microprediction.github.io/get-data.html). 

### 4. Free help 

To get you over bumps getting started, there is a slack channel and a weekly informal Google Meet, Friday's noon EST. See [get-help](https://microprediction.github.io/get-help.html). 


