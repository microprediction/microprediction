
# microprediction   ![tests](https://github.com/microprediction/microprediction/workflows/tests/badge.svg) ![deploy](https://github.com/microprediction/microprediction/workflows/deploy/badge.svg)
Looking for the microprediction [client](https://github.com/microprediction/microprediction/tree/master/microprediction) or [hello world](https://github.com/microprediction/microprediction/tree/master/hello_world)?

### Lucky you!
Running this [script](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py) makes a heck of a lot more economic sense than bitcoin mining - but few know that. There's an even gentler introduction taking the form of a [colab notebook](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/first_submission.ipynb) you can open and run now. 

# [Me](https://www.linkedin.com/in/petercotton/) and my [slack](https://join.slack.com/t/microprediction/shared_invite/zt-15mald9ph-oalX5h0wbKXRMdokGoPKZA)ing
This was supposed to be the microprediction [client](https://github.com/microprediction/microprediction/tree/master/microprediction) page! Github made this a "user page". Grumble. Well, hi this is my [dog](https://i.imgur.com/2E3pskp.jpg). This is my [blog](https://www.microprediction.com/blog). I've always worked in the private sector, though very occasionally [publish](https://scholar.google.com/citations?user=V5wB8lEAAAAJ&hl=en). My [book](https://mitpress.mit.edu/books/microprediction) is out soon. I'm dynamic and fascinating. Not really but I run a slack channel for those interested in collective open-source time-series, covariance prediction, and optimization (here's the [slack invite](https://join.slack.com/t/microprediction/shared_invite/zt-15mald9ph-oalX5h0wbKXRMdokGoPKZA)). Join the google meet Fri noon EST - see the slack. If the Slack invite requires an email domain, it has expired so DM [me](https://www.linkedin.com/in/petercotton/) on Linked-In for a new one. 

# The [TimeMachines](https://github.com/microprediction/timemachines), [Precise](https://github.com/microprediction/precise), and [HumpDay](https://github.com/microprediction/humpday) packages 

I maintain three benchmarking packages to help me, and maybe you, surf the open-source wave. 

| Topic                  | Package           | Elo ratings | Methods | Data sources | 
|------------------------|-------------------|-------------|---------|--------------| 
| Univariate time-series | [timemachines](https://github.com/microprediction/timemachines)  | [Timeseries Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_003.html) | Most popular packages ([list](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters)) | [microprediction streams](https://www.microprediction.org/browse_streams.html) |
| Global derivative-free optimization | [humpday](https://github.com/microprediction/humpday) |  [Optimizer Elo ratings](https://microprediction.github.io/optimizer-elo-ratings/html_leaderboards/overall.html) | Most popular packages ([list](https://github.com/microprediction/humpday/tree/main/humpday/optimizers)) | A mix of classic and new [objectives](https://github.com/microprediction/humpday/tree/main/humpday/objectives)      |
| Covariance, precision, correlation | [precise](https://github.com/microprediction/precise) | See [notebooks](https://github.com/microprediction/precise/tree/main/examples_colab_notebooks) | See [notebook](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/list_all_cov_methods.ipynb) |Stocks, timeseries residuals etc | 

These packages aspire to advance online autonomous prediction in a small way, but also help me notice if anyone else does!  

# The [microprediction.org](https://www.microprediction.org/) [streams](https://www.microprediction.org/browse_streams.html) ($50,000 in prediction [prizes](https://www.microprediction.com/competitions/daily))
I also maintain a *live exchange* where distributional time-series prediction algorithms (Python, R, Julia mostly) duke it out.  

- I publish live data repeatedly, [like this](https://github.com/microprediction/microprediction/blob/master/stream_examples_traffic/traffic_live.py) say, and it
 creates a stream (like [this stream](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_30_mean) or [this one](https://www.microprediction.org/stream_dashboard.html?stream=electricity-load-nyiso-overall) or any from the [listing](https://www.microprediction.org/browse_streams.html)). 
- Algorithms like [this guy](https://github.com/microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py) compete to make distributional predictions 1 min ahead, 5 min ahead, 15 min ahead and 1 hr ahead. 

In this way I can:
 - Get live prediction of public data for free (sometimes I make the "public" data obscure)
 - Indirectly benefit from [hundreds of packages](https://www.microprediction.com/blog/popular-timeseries-packages) from Github of uncertain quality, and not just Python.   

I then sip pina coladas while the accuracy magically improves over time. Read about [this example](https://medium.com/geekculture/an-empirical-article-that-wasnt-immediately-stale-720abfb4678f). 
  
### Wanna use it? 
Knock yourself out. My company funds the platform because algorithms that help solve your problem might also help solve mine. The marginal cost of their doing so is tiny. There are even [video instructions](https://www.microprediction.com/python-4).  

### Wanna make it better?

On the flip side you can:
  - Contribute predictive intelligence, win beer money (see [competitions](https://www.microprediction.com/competitions)) and then trash talk people in our slack channel. About $50,000 a year in prizes complements the scientific motivations. 
  - Automatically benchmark your work or find unexpected [uses](https://www.microprediction.org/browse_streams.html) to include in your next paper. You just need to know [how to predict data streams](https://www.microprediction.com/make-predictions), which amounts to modifying a Python script and running it. 
  
It's up to you if you choose to reveal your code. 

# [Microprediction](https://github.com/microprediction/microprediction/tree/master/microprediction) Python client


    pip install --upgrade pip
    pip install microprediction

The [client](https://github.com/microprediction/microprediction) assists use of the [microprediction api](http://api.microprediction.org/). If you don't know about the live algorithm frenzy at [microprediction.org](https://www.microprediction.org/) making this possible because you skipped down this page, did I mention that an extremely simple way to grok it is to open this colab [notebook](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/first_submission.ipynb) and run it on Google's dime? Why yes I did mention that. This will create an identity for you and enter your algorithm in an ongoing contest to predict the next roll of a die. You'll also be exactly half way to understanding the four critical pieces of functionality.  

|   | Task                                      | Method or function                | Full code example                                                                                                                                   | Video tutorial                                                                    |
|---|-------------------------------------------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| A | Create a write_key                        | new_key                           | [enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/enter_die_contest_one_off.py) | [python-1: Your first submission](https://www.microprediction.com/python-1)       |
| B | Publish one scalar value at a time, usually representing a live measurement.   | MicroWriter.set()                 | [creating_a_stream.py](https://github.com/microprediction/microtutorial/blob/master/examples/creating_a_stream.py)                                  | [python-4: Creating a stream](https://www.microprediction.com/python-4)           |
| C | Send 225 guesses of the next value of a stream, after a fixed quarantine period. | MicroWriter.submit()              | [enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/enter_die_contest_one_off.py) | [python-2: Creating your first crawler](https://www.microprediction.com/python-2) |
| D | Retrieve community predictions (PDF) 1min, 5min, 15min or 1hr ahead.            | MicroWriter.get_own_predictions() | [defassa_dog.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_golf/defassa_dog.py)                            |  [colab example](https://github.com/microprediction/microprediction/blob/master/notebook_examples/get_and_show_submitted_predictions.ipynb)                                                                                 |                  |                                                                                   |   |

Someone wanting something predicted performs A, B and D. Someone providing predictions performs A and C (mindful of the reward mechanism explained in [Collective Distributional Prediction](https://www.microprediction.com/blog/intro)).   


# [Memorable Unique Identifiers](https://github.com/microprediction/muid) and other platform repos

- The [muid](https://github.com/microprediction/muid) identifier package is explained in this [video](https://vimeo.com/397352413). 
- [microconventions](https://github.com/microprediction/microconventions) captures things common to client and server, and may answer many of your more specific questions about prediction horizons, et cetera.  
- [rediz](https://github.com/microprediction/rediz) contains server side code. For the brave. 
- There are other rats and mice like [getjson](https://github.com/microprediction/getjson), [runthis](https://github.com/microprediction/runthis) and [momentum](https://github.com/microprediction/momentum).  

# Some of my other packages: 

- [winning](https://github.com/microprediction/winning) - A recently published fast algorithm for inferring relative ability from win probability. 
- [embarrassingly](https://github.com/microprediction/embarrassingly) - A speculative approach to robust optimization that sends impure objective functions to optimizers.
- [pandemic](https://github.com/microprediction/pandemic) - Ornstein-Uhlenbeck epidemic simulation (related [paper](https://arxiv.org/abs/2005.10311))

For (American) football fans
- [firstdown](https://github.com/microprediction/firstdown) - The repo that aspires to ruin the great game of football. See Wilmott [paper](https://github.com/microprediction/firstdown/blob/main/wilmott_paper/44-49_Cotton_PDF5_Jan22%20(2).pdf).  

For M6 competitors:
- [m6](https://github.com/microprediction/m6) - Illustrates fast numerical rank probability calculations, using [winning](https://github.com/microprediction/winning). However since the rules changed, this isn't that useful for M6 anymore. There are some other resources there although you might be better served by [precise](https://github.com/microprediction/precise). Good luck. 

# Microprediction versus TimeMachines

The [TimeMachines](https://github.com/microprediction/timemachines) package is traditional open-source software for *point-estimates* and confidence, whereas the [Microprediction](https://github.com/microprediction/microprediction) client offers live crowd based *distributional* prediction. Hundreds of algorithms compete at [Microprediction](https://github.com/microprediction/microprediction) and quite a few of the [TimeMachines](https://github.com/microprediction/timemachines) algorithms (see [/skaters](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters)) are involved, drawn from packages like [river](https://github.com/online-ml/river), [pydlm](https://github.com/wwrechard/pydlm), [tbats](https://github.com/intive-DataScience/tbats), [pmdarima](http://alkaline-ml.com/pmdarima/), [statsmodels.tsa](https://www.statsmodels.org/stable/tsa.html), [neuralprophet](https://neuralprophet.com/), Facebook [Prophet](https://facebook.github.io/prophet/), 
   Uber's [orbit](https://eng.uber.com/orbit/), Facebook's [greykite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library) and more. Some are open source (look for CODE badges on [leaderboards](https://www.microprediction.org/leaderboard.html)) but others are private to their author.  
 
### StreamSkaters
 
One bridge between the [/skaters](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters) and the microprediction [leaderboards](https://www.microprediction.org/leaderboard.html) is provided by the StreamSkater class in the microprediction package, illustrated in the [StreamSkater examples](https://github.com/microprediction/microprediction/tree/master/crawler_skater_examples) folder. This makes it trivial to use any skater from the TimeMachines package in a MicroCrawler (a live algorithm). 

## More about the Microprediction Python Client
See also [README_EXAMPLES.md](https://github.com/microprediction/microprediction/blob/master/README_EXAMPLES.md) or 
[README_LONGER.md](https://github.com/microprediction/microprediction/blob/master/README_LONGER.md)

### Class Hierarchy 

Use [MicroReader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py) if you just need to get data and don't care to use a key..     

    MicroReader
       |
    MicroWriter ----------------------------
       |                                   |
    MicroPoll                         MicroCrawler
    (feed creator)               (self-navigating algorithm)
             
You can pull most data [directly](https://www.microprediction.com/public-api), by the way, without a key. 
             
### Scheduled submissions versus "crawling"
The [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) class can publish data or submit predictions. However if you intend to run a continuous process you might consider the [MicroCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/crawler.py) class or its derivatives. 

| Type                               | Suggestion                                                                                                     | Example                                                                                                                     | More examples                                                                                                                   |
|------------------------------------|----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Scheduled submission               | [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py)        | [Ambassy Fox](https://github.com/microprediction/microprediction/blob/master/submission_examples_transition/ambassy_fox.py) | [submission_examples_transition](https://github.com/microprediction/microprediction/tree/master/submission_examples_transition) |
| Running process                    | [MicroCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/crawler.py)      | [Malaxable Fox](https://github.com/microprediction/microprediction/blob/master/crawler_examples/malaxable_fox.py)           | [crawler_examples](https://github.com/microprediction/microprediction/tree/master/crawler_examples)                             |
| Running process using timemachines | [StreamSkater](https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py) | [Shole Gazelle](https://github.com/microprediction/microprediction/blob/master/crawler_examples/shole_gazelle.py)           | [crawler_skater_examples](https://github.com/microprediction/microprediction/tree/master/crawler_skater_examples)               |

A more complete picture would include [SimpleCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/simplecrawler.py), 
[RegularCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/simplecrawler.py), 
[OnlineHorizonCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/onlinecrawler.py), 
[OnlineStreamCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/onlinecrawler.py) and
[ReportingCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/reportingcrawler.py).


### Publishing absolute quantities versus changes
It is often better to publish *changes* in values than actual values of live quantities, to avoid race conditions or latency issues. There is a discussion in the [README_LONGER.md](https://github.com/microprediction/microprediction/blob/master/README_LONGER.md). 

Certainly it is easy to publish live quantities using only the [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) as shown in [traffic_live.py](https://github.com/microprediction/microprediction/blob/master/feed_examples_live/traffic_live.py). However you might consider:

- [ChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) for publishing only when values change, 
- [MultiPoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) for multiple streams
- [MultiChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py). 

### [Microprediction.Com](https://www.microprediction.com/) versus [Microprediction.org](https://www.microprediction.org/)

The former contains the [blog](https://www.microprediction.com/blog), a [knowledge center](https://www.microprediction.com/knowledge-center) with video tutorials, details of [competitions](https://www.microprediction.com/competitions) and prizemoney, and so forth. The latter is browser for humans looking to see how their algorithms are are performing, or whether their streams are updating.     

### Slack & Google Meets Tue 8pm/ Fri noon EST

Most people looking to contribute to this open initiative (and win beer money) join the [microprediction slack](https://join.slack.com/t/microprediction/shared_invite/zt-10ad1yiec-Jgsjkit~~dwNnpvRzyBTaQ). If that invite fails there might be one in the [knowledge center](https://www.microprediction.com/knowledge-center) that hasn't expired. There you will find Google Meet invite details for our regular informal chats.  

### Microprediction bookmarks

**Data**: [stream list](https://www.microprediction.org/browse_streams.html) | [stream explanations](https://www.microprediction.com/blog/livedata) | [csv](https://www.microprediction.org/features.html) **Client**: [client](https://github.com/microprediction/microprediction) | [reader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py) | [writer](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) | [crawler](https://github.com/microprediction/microprediction/blob/master/microprediction/crawler.py) | [crawler examples](https://github.com/microprediction/microprediction/tree/master/crawler_examples) | [notebook examples](https://github.com/microprediction/microprediction/tree/master/notebook_examples)
**Resources**: [popular timeseries packages](https://www.microprediction.com/blog/popular-timeseries-packages) |
[knowledge center](https://www.microprediction.com/knowledge-center) | [faq](https://www.microprediction.com/faq) |
[linked-in](https://www.linkedin.com/company/65109690) |
[microprediction.org (dashboard)](https://www.microprediction.org) | [microprediction.com (resources)](https://www.microprediction.com) |
[what](https://www.microprediction.com/what) | [blog](https://www.microprediction.com/blog) | [contact](https://www.microprediction.com/contact-us) |
[competitions](https://www.microprediction.com/competitions) |
[make-predictions](https://www.microprediction.com/make-predictions) |
[get-predictions](https://www.microprediction.com/get-predictions) |
[applications](https://www.microprediction.com/welcome-3) | [collective epidemiology](https://www.swarmprediction.com/about.html) 
**Video tutorials** : [1: non-registration](https://www.microprediction.com/python-1) | [2: first crawler](https://www.microprediction.com/python-2) |[3: retrieving historical data](https://www.microprediction.com/python-3) | [4: creating a data stream](https://www.microprediction.com/python-4) | [5: modifying your crawler's algorithm](https://www.microprediction.com/python-5) | 
[6: modifying crawler navigation](https://www.microprediction.com/python-6) 
**Colab notebooks**
[creating a new key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) |
[listing current prizes](https://github.com/microprediction/microprediction/blob/master/notebook_examples/List%20Current%20Prizes.ipynb) |
[submitting a prediction](https://github.com/microprediction/microprediction/blob/master/notebook_examples/Python_Module_1_First_Submission.ipynb) | 
[choosing streams](https://github.com/microprediction/microprediction/blob/master/notebook_examples/Crawler_choosing_streams.ipynb) |
[retrieving historical data](https://github.com/microprediction/microprediction/blob/master/notebook_examples/Python_Module_3_Getting_History.ipynb)
**Related** [humpday](https://github.com/microprediction/humpday) | [timemachines](https://github.com/microprediction/timemachines) | [timemachines-testing](https://github.com/microprediction/timemachines-testing) | [microconventions](https://github.com/microprediction/microconventions) | [muid](https://github.com/microprediction/muid) | [causality graphs](https://github.com/microprediction/microactors-causality/tree/main/gallery) | [embarrassingly](https://github.com/microprediction/embarrassingly) | [key maker](https://github.com/microprediction/keymaker) | [real data](https://github.com/microprediction/realdata)| [chess ratings prediction](https://github.com/microprediction/chess) 
**Eye candy** [copula plots](https://github.com/microprediction/microactors-plots/tree/main/gallery) | [causality plots](https://github.com/microprediction/microactors-causality/tree/main/gallery) | [electricity case study](https://www.linkedin.com/posts/rusty-conover-ba5a6_predicting-nys-electricity-using-machine-activity-6750837765761503233-vYFu) 

Probably best to start in the [knowledge center](https://www.microprediction.com/knowledge-center) and remember [Dorothy, You're Not in Kaggle Anymore](https://www.linkedin.com/pulse/dorothy-youre-kaggle-anymore-peter-cotton-phd/). 

  
### Cite
See [CITE.md](https://github.com/microprediction/microprediction/blob/master/CITE.md)

### FAQ:
[FAQ](https://www.microprediction.com/faq) 

### Video tutorials
See the [Knowledge Center](https://www.microprediction.com/knowledge-center)

### Hey, where did the old README go? 

[README_LONGER.md](https://github.com/microprediction/microprediction/blob/master/README_LONGER.md)





