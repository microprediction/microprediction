# microprediction

Client library for www.microprediction.org You publish live data repeatedly, and it gets predicted. Simple, eh? 
Tap into the collective intelligence of community contributed time series algorithms, or add to the intelligence. 


    pip install microprediction 
    
This library can also be used to submit predictions.

## Participate immediately with a bash script

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/microprediction/master/shell_examples/run_default_crawler_from_new_venv.sh)"

## Hello world examples

- https://github.com/microprediction/microprediction/tree/master/hello_world

## Getting help 

- https://www.microprediction.org/contact.html
- https://github.com/microprediction/microprediction/issues 
  

## Site documentation at Microprediction.Org
    
- https://www.microprediction.org/publishing.html 

- https://www.microprediction.org/crawling.html

Questions to  info@microprediction.org 

### New skin coming soon...


![](https://i.imgur.com/6FpjUaR.png)

## Class Hierarchy 

Provided classes include the following

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

                          
      
## Quickstart: Soliciting predictions 

If you have a function that returns a live number, do this:

```python
    from microprediction import MicroPoll, create_key
    feed = MicroPoll(write_key=create_key(),        # This takes a while ... see section on mining write_keys below
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

Here is an actual example: 
https://www.microprediction.org/stream_dashboard.html?stream=fcx&horizon=70 for a 1 minute ahead CDF. If you wish to use the Python client:

```python
         cdf = feed.get_cdf('cop.json',delay=70,values=[0,0.5])
```
         
where the delay parameter, in seconds, is the prediction horizon (it is called a delay as the predictions used to compute this CDF have all be quarantine for 70 seconds or more). 
The community of algorithms provides predictions roughly 1 min, 5 min, 15 minutes and 1 hr ahead of time. The `get_cdf()` above reveals the probability that your future value is less than 0.0, and the probability that it is 
less than 0.5. You can view CDFs and activity at MicroPrediction.Org by entering your write key in the dashboard. 


## Z-Scores

A bonus! Based on algorithm predictions, every data point you publish creates another two streams, representing community z-scores for your data 
point based on predictions made at different times prior (those quarantined the shortest, and longest intervals). 

|  Stream                                      |                                                                                   |
|----------------------------------------------|-----------------------------------------------------------------------------------|
|  Base stream                                 |  `https://www.microprediction.org/stream_dashboard.html?stream=cop`               |
|  Z-score relative to 70s ahead predictions   |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~cop~70`         |
|  Z-score relative to 3555s ahead predictions  |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~cop~3555`        |

In turn, each of these streams is predicted at four different horizons, as with the base stream. For example: 

| Stream       |   Roughly 1 min ahead           | Roughly 5 min ahead                 |   Roughly 15 min ahead              | Roughly 1 hr ahead |
|--------------|---------------------------------|-------------------------------------|-------------------------------------|---------------------
| cop          | `stream=cop&horizon=70`         |  `stream=cop&horizon=310`           | `stream=cop&horizon=910`            | `stream=cop&horizon=3555` 
| `z1~cop~3555`| `stream=z1~cop~3555&horizon=70` |  `stream=z1~cop~3555&horizon=310`   | `stream=z1~cop~3555&horizon=910`    | `stream=z1~cop~3555&horizon=3555'
  
     
## Quickstart: Providing predictions 

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

It is possible to retrieve most quantities at api.microprediction.org with direct web calls such as https://api.microprediction.org/live/cop.json. Use your preferred means such as requests or aiohttp. For example using the former:

```python
    import requests
    lagged_values = requests.get('https://api.microprediction.org/live/lagged_values::cop.json').json()
    lagged        = requests.get('https://api.microprediction.org/lagged/cop.json').json()
```

However the reader client adds a little convenience. 

```python
    from microprediction import MicroReader
    mr = MicroReader()
 
    current_value = mr.get('cop.json')
    lagged_values = mr.get_lagged_values('cop.json') 
    lagged_times  = mr.get_lagged_times('cop.json')
```

Your best reference for the API is the client code https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py 
    
## Write client

As noted above you may prefer to use MicroPoll or MicroCrawler rather than MicroWriter directly. But here are a few more details on the API wrapper those wanting more control. You can create predictions or feeds using only
the writer. Your best reference is the client code https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py 

### Instantiate a writer 

In principle:

```python
    from microprediction import MicroWriter, create_key
    mw = MicroWriter(write_key=create_key(difficulty=12))    # Sub in your own write_key. MUIDs explained at https://vimeo.com/397352413 
```

In practice you may want to run create_key() separately as it will take many hours, at least for a difficult key. See https://config.microprediction.org/config.json for the current values of min_len, which is the official minimum difficulty to create a stream. If you don't need
to create streams but only wish to predict, you can use a lower difficulty like 10 or even 9. But the easier your key, the more likely
you are to go bankrupt. 
    
### Submitting scenarios (manually)
    
If MicroCrawler does not suit your needs you can submit predictions:

```python
    scenarios = [ i*0.001 for i in range(mw.num_predictions) ]   # You can do better ! 
    mw.submit(name='cop.json',values=scenarios, delay=70)        # Specify stream name and also prediction horizon
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
        
1. Check https://github.com/microprediction/microconventions/blob/master/microconventions/stream_conventions.py to see if you are violating a stream naming convention
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
On an ongoing basis you also need the `write_key` balance not to fall below a threshold bankruptcy level. The minimum balance for a key of difficulty 9 is also found at https://api.microprediction.org/config.json and the formula:

<img src="https://render.githubusercontent.com/render/math?math=%5CLarge%0A-1*(abs(self.min%5C_balance)*16%5E%7B(write%5C_key%5C_difficulty-9)%7D">

supercedes whatever is written here. However at time of writing the bankruptcy levels are:

|  write_key difficulty   |  bankruptcy         |  write_key difficulty   |  bankruptcy         |
|-------------------------|---------------------|-------------------------|---------------------|
|  8                      |  -0.01              |     11                  |   -256              |
|  9                      |  -1.0               |     12                  |   -4,096            |
| 10                      |  -16.0              |     13                  |   -65,536           |
       
Balance may be transfered from one `write_key` to another if the recipient `write_key` has a negative balance. You can use the transfer function to keep
a `write_key` alive that you need for sponsoring a stream. You can also ask others to mine (muids)[https://github.com/microprediction/muid] for you and contribute in this fashion, say if you have an important civic nowcast and expect that others
 might help maintain it. You cannot use a transfer to 
raise the balance associated with a `write_key` above zero - that is only possible by means of accurate prediction. 

## Advanced topic: Higher dimensional prediction with `cset()` 

Multivariate prediction solicitation is available to those with write_keys of difficulty 1 more than the stream minimum (i.e. 12+1). If you want to use this we suggest you start mining now. My making regular calls
 to `mw.cset()` you can get all these goodies automatically:
         
|  Functionality          |  Example dashboard URL                                                            |
|-------------------------|-----------------------------------------------------------------------------------|
|  Base stream #1         |  `https://www.microprediction.org/stream_dashboard.html?stream=cop`               |
|  Base stream #2         |  `https://www.microprediction.org/stream_dashboard.html?stream=fcx`               |
|  Z-scores               |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~cop~310`        |
|  Bivariate copula       |  `https://www.microprediction.org/stream_dashboard.html?stream=z2~cop~pe~910`     |
|  Trivariate copula      |  `https://www.microprediction.org/stream_dashboard.html?stream=z3~cop~fcx~pe~910` |         
         
Copula time series are univariate. An embedding from R^3 or R^2 to R is used (Morton space filling Z-curve). The most up to date
reference for these embeddings is at https://github.com/microprediction/microconventions/blob/master/microconventions/zcurve_conventions.py
         
  
## More examples 

- https://github.com/microprediction/microprediction/blob/master/README_EXAMPLES.md       

## Suggested reading

- https://www.linkedin.com/pulse/short-introduction-z-streams-peter-cotton-phd/
- https://www.linkedin.com/pulse/dorothy-youre-kaggle-anymore-peter-cotton-phd/
- https://www.linkedin.com/pulse/live-online-distribution-estimation-using-t-digests-peter-cotton-phd/
- https://www.linkedin.com/pulse/can-one-line-python-win-contest-micropredictionorg-peter-cotton-phd/
- https://www.linkedin.com/pulse/call-contributions-copula-contest-where-carefully-can-cotton-phd/
- https://www.linkedin.com/pulse/where-badminton-player-move-next-how-should-we-same-peter-cotton-phd/
- https://www.linkedin.com/pulse/helicopulas-peter-cotton-phd/

See [article list](https://www.linkedin.com/in/petercotton/detail/recent-activity/posts/)
