# microprediction

Hi. This is the client library for www.microprediction.org, humble birthplace of the prediction web. Some people call it "Napster meets DataRobot". It challenges
the Automated Machine Learning industry, and mocks artisan data science. We have quite a few things planned. For now, however, a time series focus and here's what's up: 

- You publish live data repeatedly, [like this](https://github.com/microprediction/microprediction/blob/master/feed_examples_live/traffic_live.py) say, and it
 creates a stream like [this one](https://www.microprediction.org/stream_dashboard.html?stream=electricity-load-nyiso-overall).
- As soon as you do, algorithm "crawlers" like [this guy](https://github.com/microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py) compete to make distributional predictions of
your data feed 1 min ahead, 5 min ahead, 15 min ahead and 1 hr ahead. 

In this way you can:
 - Get live prediction of public data for free (yes it really is an [api](http://api.microprediction.org/) that predicts anything!)
 - See which R, Julia and Python time series approaches seem to work best, saving you from
  trying out [hundreds of packages](https://www.microprediction.com/blog/popular-timeseries-packages) from PyPI and github of uncertain quality. 
  
Here's a [first glimpse](https://www.microprediction.com/welcome) for the uninitiated, some [categories of business application](https://www.microprediction.com/welcome-3), some remarks
on why [microprediction is synomymous with AI](https://www.microprediction.com/welcome-4) due to the possibility of value function prediction, and a straightforward
[plausibility argument](https://www.microprediction.com/welcome-2) for why an open source, openly networked collection of algorithms that 
are perfectly capable of [managing each other](https://www.microprediction.com/welcome-5) will sooner or later eclipse all other modes of production
of prediction. In order to try to get this idea off the ground, there are some ongoing [competitions](https://www.microprediction.com/competitions) and developer incentives. 
    
## Video tutorials
    
Video tutorials are available at https://www.microprediction.com/python-1 to help you
get started. There's a video explanation of FitCrawler, SequentialCrawler and friends
at https://www.microprediction.com/fitcrawler.     
    
## Presentations

Presentations at Rutgers, MIT and elsewhere can be found in the [presentations](https://github.com/microprediction/micropresentations) repo. A book will be 
published by MIT Press in 2021 on the topic. There are links to video presentations in some of the [blog](https://www.microprediction.com/blog) articles. 

![](https://i.imgur.com/uwttTku.png)


## (New!) Knowledge Center

See the [knowledge center](https://www.microprediction.com/knowledge-center) for a structured set of [Python tutorials](https://www.microprediction.com/python-1) which will 
show you how to create an identity, enter a live contest and use the [dashboard](https://www.microprediction.org/) to track your algorithms' progress. It will also show you how
to [retrieve historical data](https://www.microprediction.com/python-3) for time series research, if that is the only way you wish to use the site. You don't have to use
Python because the [api](api.microprediction.org) can be accessed in any language. We have contributors using Julia ([example](https://github.com/rustyconover/microprediction-nyiso-electricity)) and 
you can even enter using R from within Kaggle ([tutorial](https://www.microprediction.com/r-1)).   


## Participate immediately with a bash script
Linux and mac users can run the default crawler with a one line cut and paste. This will use a virtual environment, and thus not interfere with your other work.  

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/microprediction/master/shell_examples/run_default_crawler_from_new_venv.sh)"

It's a great way to quickly get the joke. You should intend to run this "forever".
## Examples, examples, examples

- [hello world](https://github.com/microprediction/microprediction/tree/master/hello_world) feed creation and submission. 
- [notebooks](https://github.com/microprediction/microprediction/tree/master/notebook_examples) are available too, but these are harder to run indefinitely
- [crawler examples](https://github.com/microprediction/microprediction/tree/master/crawler_examples)

Pro tip: Look at the [leaderboards](https://www.microprediction.org/leaderboard.html) and click on CODE badges. Fork an algorithm that is doing well.  

## Discussion and help

- [discussions on github](https://github.com/microprediction/microprediction/discussions)  (new!)
- [contact](https://www.microprediction.com/contact-us) us to be included in Friday noon contributor chat (very informal)
- [issues](https://github.com/microprediction/microprediction/issues) 
- [![Gitter](https://badges.gitter.im/microprediction/community.svg)](https://gitter.im/microprediction/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)  

### Frequently asked questions

- Moved to [FAQ](https://www.microprediction.com/faq)
- See also the [Knowledge Center](https://www.microprediction.com/knowledge-center)

## Class Hierarchy 

Use MicroReader if you just need to get data and don't care to use a key. Create streams [like this](https://github.com/microprediction/microprediction/blob/master/feed_examples_live/traffic_live.py) using
the MicroWriter, or its sub-classes. You can also use MicroWriter to submit predictions, though MicroCrawler adds some conveniences. 

    MicroReader
       |
    MicroWriter ----------------------------
       |                                   |
    MicroPoll                         MicroCrawler
    (feed creator)               (self-navigating algorithm)
                
A more complete picture would include [SimpleCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/simplecrawler.py), 
[RegularCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/simplecrawler.py), 
[OnlineHorizonCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/onlinecrawler.py), 
[OnlineStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/onlinecrawler.py) and
[ReportingCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/reportingcrawler.py), as well
as additional conveniences for creating streams such as 
[ChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py), [MultiPoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py),
and [MultiChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py).

                          
## Quickstart: Creating a stream to publish a number every 20 minutes

If you have a function that returns a live number, you can do this

```python
    from microprediction import MicroPoll
    feed = MicroPoll(difficulty=12,                 # This takes a long time ... see section on mining write_keys below
                     name='my_stream.json',         # Name your data stream
                     func=my_feed_func,             # Provide a callback function that returns a float 
                     interval=20)                   # Poll every twenty minutes
    feed.run()                                      # Start the scheduler
``` 
    
## Retrieving distributional predictions 
Once a stream is created and some crawlers have found it, you can view activity and predictions at www.microprediction.org, 

| Stream      |   Roughly 1 min ahead           | Roughly 5 min ahead             |   Roughly 15 min ahead               | Roughly 1 hr  ahead               |
|-------------|---------------------------------|---------------------------------|--------------------------------------|-----------------------------------|
| my_stream   | `stream=my_stream&horizon=70`   |  `stream=my_stream&horizon=310` | `stream=my_stream&horizon=910`       | `stream=my_stream&horizon=3555`   | 

Full URL example: https://www.microprediction.org/stream_dashboard.html?stream=c5_iota&horizon=70 for a 1 minute ahead CDF. If you wish to use the Python client:

```python
         cdf = feed.get_cdf('cop.json',delay=70,values=[0,0.5])
```
         
where the delay parameter, in seconds, is the prediction horizon (it is called a delay as the predictions used to compute this CDF have all be quarantine for 70 seconds or more). 
The community of algorithms provides predictions roughly 1 min, 5 min, 15 minutes and 1 hr ahead of time. The `get_cdf()` above reveals the probability that your future value is less than 0.0, and the probability that it is 
less than 0.5. You can view CDFs and activity at MicroPrediction.Org by entering your write key in the dashboard. 


## Z-Scores

Now we're getting into the fancy stuff. 

Based on algorithm predictions, every data point you publish creates another two streams, representing community z-scores for your data 
point based on predictions made at different times prior (those quarantined the shortest, and longest intervals). 

|  Stream                                      |                                                                                   |
|----------------------------------------------|-----------------------------------------------------------------------------------|
|  Base stream                                 |  `https://www.microprediction.org/stream_dashboard.html?stream=c5_iota`               |
|  Z-score relative to 70s ahead predictions   |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~c5_iota~70`         |
|  Z-score relative to 3555s ahead predictions  |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~c5_iota~3555`        |

In turn, each of these streams is predicted at four different horizons, as with the base stream. For example: 

| Stream       |   Roughly 1 min ahead           | Roughly 5 min ahead                 |   Roughly 15 min ahead              | Roughly 1 hr ahead |
|--------------|---------------------------------|-------------------------------------|-------------------------------------|---------------------
| c5_iota          | `stream=c5_iota&horizon=70`         |  `stream=c5_iota&horizon=310`           | `stream=c5_iota&horizon=910`            | `stream=c5_iota&horizon=3555` 
| `z1~c5_iota~3555`| `stream=z1~c5_iota~3555&horizon=70` |  `stream=z1~c5_iota~3555&horizon=310`   | `stream=z1~c5_iota~3555&horizon=910`    | `stream=z1~c5_iota~3555&horizon=3555`
  
Poke around the [stream listing](https://www.microprediction.org/browse_streams.html) near the bottom and you'll see them. 
     
# A Quick Guide to Crawling and the API/Client

See also the [public api](https://www.microprediction.com/public-api) guide. 

## Let your algorithm loose on the world 

If you have a function that takes a vector of lagged values of a time series and supplies a *distributional* prediction, a fast way to get going is
deriving from MicroCrawler as follows: 

 
```python 
    from microprediction import MicroCrawler, create_key
    from microprediction.samplers import differenced_bootstrap
    
    class MyCrawler(MicroCrawler):
    
        def sample(self, lagged_values, lagged_times=None, name=None, delay=None):
            my_point_estimate = 0.75*lagged_values[0]+0.25*lagged_values[1]                                     # You can do better
            scenarios = differenced_bootstrap(lagged=lagged_values,  decay=0.01, num=self.num_predictions)      # You can do better
            samples = [ my_point_estimate+s for s in scenarios ]
            return samples

    my_write_key = create_key(difficulty=11)   # Be patient. Maybe visit www.MUID.org to learn about Memorable Unique Identifiers 
    print(my_write_key)
    crawler = MyCrawler(write_key=write_key)
    crawler.run()
```

Enter your write_key into https://www.microprediction.org/dashboard.html to find out which time series your crawler is good at predicting. Check back in a day, a week or a month. 
 

## Read client

It is possible to retrieve most quantities at api.microprediction.org with direct web calls such as https://api.microprediction.org/live/c5_iota.json. Use your preferred means such as requests or aiohttp. For example using the former:

```python
    import requests
    lagged_values = requests.get('https://api.microprediction.org/live/lagged_values::c5_iota.json').json()
    lagged        = requests.get('https://api.microprediction.org/lagged/c5_iota.json').json()
```

However the reader client adds a little convenience. 

```python
    from microprediction import MicroReader
    mr = MicroReader()
 
    current_value = mr.get('c5_iota.json')
    lagged_values = mr.get_lagged_values('c5_iota.json') 
    lagged_times  = mr.get_lagged_times('c5_iota.json')
```

Your best reference for the API is the client code https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py 
    
## Write client

As noted above you may prefer to use MicroPoll or MicroCrawler rather than MicroWriter directly. But here are a few more details on the API wrapper those wanting more control. You can create predictions or feeds using only
the writer. Your best reference is the client code https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py 

### Instantiate a writer 

In principle:

```python
    from microprediction import MicroWriter
    mw = MicroWriter(difficulty=12)    # Creates new key on the fly, slowly! MUIDs explained at https://vimeo.com/397352413 
```

But better to do 

```python
      from microprediction import new_key
      write_key = new_key(difficulty=12)
```
separately, then pass in with 
```python
      mw = MicroWriter(write_key=write_key)
```

Thing is, new_key() will take many hours and that avoids the system being flooded with spurious streams. See https://config.microprediction.org/config.json for
 the current values of min_len, which is the official minimum difficulty to create a stream. If you don't need
to create streams but only wish to predict, you can use a lower difficulty like 10 or even 9. But the easier your key, the more likely
you are to go bankrupt (read on).
    
### Submitting scenarios (manually)
    
If MicroCrawler does not float your boat, you can design your own way to monitor streams and make predictions using MicroWriter. 
 
```python
    scenarios = [ i*0.001 for i in range(mw.num_interp) ]   # You can do better ! 
    mw.submit(name='c5_iota.json',values=scenarios, delay=70)        # Specify stream name and also prediction horizon
```

See https://config.microprediction.org/config.json for a list of values that delay can take. 

### Creating a feed (manually)

If MicroPoll does not serve your needs you can create your stream one data point at a time:

```python
    mw  = MicroWriter(write_key=write_key)
    res = mw.set(name='mystream.json',value=3.14157) 
```

However if you don't do this regularly, your stream's history will die and you will lose rights to the name 'mystream.json' established when you made the first call. If you have a long break between data points, such
 as overnight or over the weekend, consider
touching the data stream:

```python
    res = mw.touch(name='mystream.json')
```

to let the system know you still care.  

### Troubleshooting stream creation
        
0. Upgrade the library, which is pretty fluid
   1. `pip install --upgrade microprediction`
        
1. Check [stream_conventions](https://github.com/microprediction/microconventions/blob/master/microconventions/stream_conventions.py) to see if you are violating a stream naming convention
   1. Must end in `.json`  
   2. Must contain only alphanumeric, hyphens, underscores, colons (discouraged) and at most one period.
   3. Must not contain double colon. 
   
2. Log into Dashboard with your write_key:
   1. https://www.microprediction.org/dashboard.html
   2. Check for errors/warnings You can also use `mw.get_errors()`, `mw.get_warnings()`, `mw.get_confirmations()`
   3. Was the name already taken? 
   4. Is your `write_key` bankrupt? 

## Mining write_keys 

Want more write keys? Cut and paste this bash command into a bash shell:

```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/muid/master/examples/mine_from_venv.sh)"
```

or use the MUID library (www.muid.org) ...

```
    $pip install muid
    $python3
    >>> import muid
    >>> muid.mine(skip_intro=True)
```

See www.muid.org or https://vimeo.com/397352413 for more on MUIDs. Use a URL like http://www.muid.org/validate/fb74baf628d43892020d803614f91f29 to 
reveal the hidden "spirit animal" in a MUID. The difficulty is the length of the animal, not including the space.     

        
## Balances and bankruptcy 

Every participating `write_key` has an associated balance. When you create a stream you automatically participate in the prediction of the stream. A benchmark empirical sampling algorithm with some recency adjustment is used for this
purpose. If nobody can do a better job that this, your `write_key` balance will neither rise nor fall, on average.  

However once smart people and algorithms enter the fray, you can expect this default model to be beaten and the balance on your `write_key` to trend downwards. 
On an ongoing basis you also need the `write_key` balance not to fall below a threshold bankruptcy level. The minimum balance for a key of difficulty 9 is also found at https://api.microprediction.org/config.json and
 the formula:
 

<img src="https://render.githubusercontent.com/render/math?math=%5CLarge%0A-1*(abs(self.min%5C_balance)*16%5E%7B(write%5C_key%5C_difficulty-9)%7D">


supercedes whatever is written here. However, at time of writing the bankruptcy levels are:

|  write_key difficulty   |  bankruptcy         |  write_key difficulty   |  bankruptcy         |
|-------------------------|---------------------|-------------------------|---------------------|
|  8                      |  -0.01              |     11                  |   -256              |
|  9                      |  -1.0               |     12                  |   -4,096            |
| 10                      |  -16.0              |     13                  |   -65,536           |
       
You can see why your crawler may live a longer life if the key is more difficult. 

Balance may be transferred from one `write_key` to another if the recipient `write_key` has a negative balance. You can use the transfer function to keep
a `write_key` alive that you need for sponsoring a stream. You can also ask others to mine (muids)[https://github.com/microprediction/muid] for you and contribute in this fashion, say if you have an important civic nowcast and expect that others
 might help maintain it. You cannot use a transfer to 
raise the balance associated with a `write_key` above zero - that is only possible by means of accurate prediction. 

## Advanced topic: Higher dimensional prediction with `cset()` 

Multivariate prediction solicitation is available to those with write_keys of difficulty 1 more than the stream minimum (i.e. 12+1). If you want to use this we suggest you start mining now. My making regular calls
 to `mw.cset()` you can get all these goodies automatically:
         
|  Functionality          |  Example dashboard URL                                                            |
|-------------------------|-----------------------------------------------------------------------------------|
|  Base stream #1         |  `https://www.microprediction.org/stream_dashboard.html?stream=c5_iota`               |
|  Base stream #2         |  `https://www.microprediction.org/stream_dashboard.html?stream=c5_bitcoin`               |
|  Z-scores               |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~c5_iota~310`        |
|  Bivariate copula       |  `https://www.microprediction.org/stream_dashboard.html?stream=z2~c5_iota~pe~910`     |
|  Trivariate copula      |  `https://www.microprediction.org/stream_dashboard.html?stream=z3~c5_iota~c5_bitcoin~pe~910` |         
         
Copula time series are univariate. An embedding from R^3 or R^2 to R is used (Morton space filling Z-curve). The most up to date
reference for these embeddings is the code (see [zcurve_conventions](https://github.com/microprediction/microconventions/blob/master/microconventions/zcurve_conventions.py) ). There is
a little video of the embedding in the (FAQ)[https://www.microprediction.com/faq]. 
         
## Follow and help

This project is socialized mostly via Linked-In. See 
[microprediction](https://www.linkedin.com/company/65109690) and other articles. You can 
help in a small way by celebrating posts and articles like this, should you be so inclined. 

- [Introduction to Z-Streams](https://www.linkedin.com/pulse/short-introduction-z-streams-peter-cotton-phd/)
- [Dorothy, You're Not in Kaggle Anymore](https://www.linkedin.com/pulse/dorothy-youre-kaggle-anymore-peter-cotton-phd/)
- [Online Distributional Estimation](https://www.linkedin.com/pulse/live-online-distribution-estimation-using-t-digests-peter-cotton-phd/)
- [Win With One Line of Code](https://www.linkedin.com/pulse/can-one-line-python-win-contest-micropredictionorg-peter-cotton-phd/)
- [Copulas and Crypto](https://www.linkedin.com/pulse/call-contributions-copula-contest-where-carefully-can-cotton-phd/)
- [Badminton](https://www.linkedin.com/pulse/where-badminton-player-move-next-how-should-we-same-peter-cotton-phd/)
- [Helicopulas](https://www.linkedin.com/pulse/helicopulas-peter-cotton-phd/)

See [article list](https://www.linkedin.com/in/petercotton/detail/recent-activity/posts/)



## Further reading

See the [Knowledge Center](https://www.microprediction.com/knowledge-center) and [blog](https://www.microprediction.com/blog) for listings of time series algorithms,
comparisons of global hyper-parameter optimizers and other tips.   

## PS: Don't mind the litter

There are some mostly unrelated notebooks for www.microprediction.com/blog that will be 
moved when I have a moment. 
