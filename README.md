
# microprediction user homepage ![tests](https://github.com/microprediction/microprediction/workflows/tests/badge.svg) ![deploy](https://github.com/microprediction/microprediction/workflows/deploy/badge.svg) 
Looking for the microprediction [docs](https://microprediction.github.io/microprediction/), [client](https://github.com/microprediction/microprediction/tree/master/microprediction) or [hello world](https://github.com/microprediction/microprediction/tree/master/hello_world)

# [Me](https://github.com/microprediction/home), my [slack](https://microprediction.github.io/microprediction/slack.html) and [I](https://www.linkedin.com/in/petercotton/)

This was supposed to be the microprediction [client](https://github.com/microprediction/microprediction/tree/master/microprediction) page. Github made this a "user page". Well, hi this is my [dog](https://i.imgur.com/2E3pskp.jpg). This is my [blog](https://www.microprediction.com/blog). This page describes some of my open-source projects. 
I've always worked in the private sector, though very occasionally [publish](https://scholar.google.com/citations?user=V5wB8lEAAAAJ&hl=en). My [book](https://mitpress.mit.edu/books/microprediction) is out soon and here's a list of other 
[stuff I've written](https://github.com/microprediction/home). 

I'm dynamic and fascinating. Not really but I run a
slack channel for those interested in collective open-source time-series, covariance
prediction, optimization and things enabling
collective microprediction. You're [invited](https://microprediction.github.io/microprediction/slack.html) to that and
weekly informal Google meets on Fridays noon EST - see the slack. If the
Slack invite requires an email domain, it has
expired so DM [me](https://www.linkedin.com/in/petercotton/) on Linked-In
for a new one. 

Should you be interested in microprediction? Well if nothing else, I'll 
point out that due to its obscurity, running this [script](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py) makes a heck of a lot more economic sense than bitcoin mining - 
try it out or see the [docs](https://microprediction.github.io/microprediction).

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

- I publish live data repeatedly, [like this](https://github.com/microprediction/microprediction/blob/master/stream_examples_traffic/traffic_speed.py) say, and it
 creates a stream (like [this stream](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_30_mean) or [this one](https://www.microprediction.org/stream_dashboard.html?stream=electricity-load-nyiso-overall) or any from the [listing](https://www.microprediction.org/browse_streams.html)). 
- Algorithms like [this guy](https://github.com/microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py) compete to make distributional predictions 1 min ahead, 5 min ahead, 15 min ahead and 1 hr ahead. 

In this way I can:
 - Get live prediction of public data for free (sometimes I make the "public" data obscure)
 - Indirectly benefit from [hundreds of packages](https://www.microprediction.com/blog/popular-timeseries-packages) from Github of uncertain quality, and not just Python.
 - Sip pina coladas while the accuracy magically improves over time. Read about [this example](https://medium.com/geekculture/an-empirical-article-that-wasnt-immediately-stale-720abfb4678f). 
  
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
 



