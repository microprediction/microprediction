
# microprediction [client](https://github.com/microprediction/microprediction/tree/master/microprediction), [docs](https://microprediction.github.io/microprediction/), and [examples](https://github.com/microprediction/microprediction) ![tests](https://github.com/microprediction/microprediction/workflows/tests/badge.svg) ![deploy](https://github.com/microprediction/microprediction/workflows/deploy/badge.svg) 
The [docs](https://microprediction.github.io/microprediction/) include [install](https://microprediction.github.io/microprediction/install.html) instructions or a way to complain about [issues with my book](https://github.com/microprediction/building_an_open_ai_network)? This was supposed to be the microprediction [client](https://github.com/microprediction/microprediction/tree/master/microprediction) README. Github made this a "user page". They know best. Well then hi this is my [dog](https://microprediction.github.io/microprediction/slack.html). This is my [blog](https://www.microprediction.com/blog). I've always worked in the private sector, though very occasionally [publish](https://scholar.google.com/citations?user=V5wB8lEAAAAJ&hl=en). My [book](https://mitpress.mit.edu/books/microprediction) is out soon and here's a list of other [stuff I've written](https://github.com/microprediction/home). 

I'm dynamic and fascinating. Not really but I run a slack channel for those interested in time-series, covariance
prediction, optimization and other things enabling semi-autonomous collective microprediction. Most Friday's at noon
I make myself available to anyone interesting in these things via a regular open google meet (see [here](https://microprediction.github.io/microprediction/meet.html)). I'm not big on booking things
on my calendar, ever, as there is no way to predict in advance if a given 15 minute product pitch will derail continguous work. Thanks
for you understanding. 

# The [TimeMachines](https://github.com/microprediction/timemachines), [Precise](https://github.com/microprediction/precise), and [HumpDay](https://github.com/microprediction/humpday) packages 

I maintain three benchmarking packages to help me, and maybe you, surf the open-source wave. 

| Topic                  | Package           | Elo ratings | Methods                                                                                                                                                                                  | Data sources | 
|------------------------|-------------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------| 
| Univariate time-series | [timemachines](https://github.com/microprediction/timemachines)  | [Timeseries Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_003.html) | Most popular packages ([list](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters))                                                                           | [microprediction streams](https://www.microprediction.org/browse_streams.html)                                      |
| Global derivative-free optimization | [humpday](https://github.com/microprediction/humpday) |  [Optimizer Elo ratings](https://microprediction.github.io/optimizer-elo-ratings/html_leaderboards/overall.html) | Most popular packages ([list](https://github.com/microprediction/humpday/tree/main/humpday/optimizers))                                                                                  | A mix of classic and new [objectives](https://github.com/microprediction/humpday/tree/main/humpday/objectives)      |
| Covariance, precision, correlation | [precise](https://github.com/microprediction/precise) | See [notebooks](https://github.com/microprediction/precise/tree/main/examples_colab_notebooks) | [cov](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md) and [portfolio](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md) lists |Stocks, electricity etc                                                                                              | 

These packages aspire to advance online autonomous prediction in a small way, but also help me notice if anyone else does!  

# The [microprediction.org](https://www.microprediction.org/) platform
Yes I maintain a *live exchange* where distributional time-series prediction
 algorithms (Python, R, Julia mostly) duke it out, trying to predict future values of [streams](https://www.microprediction.org/browse_streams.html). But after reiterating that there is $50,000 in prediction [prizes](https://www.microprediction.com/competitions/daily) up for grabs (wow that's incredible!) I'll send you to the better organized [documentation](https://microprediction.github.io/microprediction/) that supercedes this README. 

No? Okay fine. TLDR:

- I publish live data repeatedly, [like this](https://github.com/microprediction/microprediction/blob/master/stream_examples_traffic/traffic_speed.py) say, and it
 creates a stream (like [this stream](https://www.microprediction.org/stream_dashboard.html?stream=c2_rebalanced_30_mean) or [this one](https://www.microprediction.org/stream_dashboard.html?stream=electricity-load-nyiso-overall) or any from the [listing](https://www.microprediction.org/browse_streams.html)). 
- Algorithms like [this guy](https://github.com/microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py) compete to make distributional predictions 1 min ahead, 5 min ahead, 15 min ahead and 1 hr ahead. 

In this way I can:
 - Get live prediction of public data for free (sometimes I make the "public" data obscure)
 - Indirectly benefit from [hundreds of packages](https://www.microprediction.com/blog/popular-timeseries-packages) from Github of uncertain quality, and not just Python.
 - Sip pina coladas while the accuracy magically improves over time. Read about [this example](https://medium.com/geekculture/an-empirical-article-that-wasnt-immediately-stale-720abfb4678f). 

Should you be interested in helping micropredict stuff? Well if nothing else, I'll 
point out that due to its obscurity, running this [script](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py) makes a heck of a lot more economic sense than bitcoin mining - 
try it out or see the [docs](https://microprediction.github.io/microprediction).
  
Just to lean on the differences between this and the other benchmarking efforts, the [TimeMachines](https://github.com/microprediction/timemachines) package is traditional open-source software for *point-estimates* and confidence, whereas the [Microprediction](https://github.com/microprediction/microprediction) client offers live crowd based *distributional* prediction and also, in theory, exogenous data search. But the similarity
is that hundreds of algorithms compete at [Microprediction](https://github.com/microprediction/microprediction) and quite a few of the [TimeMachines](https://github.com/microprediction/timemachines) algorithms (see [/skaters](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters)) are involved, drawn from packages like [river](https://github.com/online-ml/river), [pydlm](https://github.com/wwrechard/pydlm), [tbats](https://github.com/intive-DataScience/tbats), [pmdarima](http://alkaline-ml.com/pmdarima/), [statsmodels.tsa](https://www.statsmodels.org/stable/tsa.html), [neuralprophet](https://neuralprophet.com/), Facebook [Prophet](https://facebook.github.io/prophet/), 
   Uber's [orbit](https://eng.uber.com/orbit/), Facebook's [greykite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library) and more. Some are open source (look for CODE badges on [leaderboards](https://www.microprediction.org/leaderboard.html)) but others are private to their author.  

# [Memorable Unique Identifiers](https://github.com/microprediction/muid) and other platform repos

- The [muid](https://github.com/microprediction/muid) identifier package is explained in this [video](https://vimeo.com/397352413). 
- [microconventions](https://github.com/microprediction/microconventions) captures things common to client and server, and may answer many of your more specific questions about prediction horizons, et cetera.  
- [rediz](https://github.com/microprediction/rediz) contains server side code. For the brave. 
- There are other rats and mice like [getjson](https://github.com/microprediction/getjson), [runthis](https://github.com/microprediction/runthis) and [momentum](https://github.com/microprediction/momentum).  

# Some of my other packages: 

- [winning](https://github.com/microprediction/winning) - A recently published fast algorithm for inferring relative ability from win probability. 
- [embarrassingly](https://github.com/microprediction/embarrassingly) - A speculative approach to robust optimization that sends impure objective functions to optimizers.
- [pandemic](https://github.com/microprediction/pandemic) - Ornstein-Uhlenbeck epidemic simulation (related [paper](https://arxiv.org/abs/2005.10311))
- [firstdown](https://github.com/microprediction/firstdown) - The repo that aspires to ruin the great game of football. See Wilmott [paper](https://github.com/microprediction/firstdown/blob/main/wilmott_paper/44-49_Cotton_PDF5_Jan22%20(2).pdf).  
- [m6](https://github.com/microprediction/m6) - Illustrates fast numerical rank probability calculations, using [winning](https://github.com/microprediction/winning). However since the rules changed, this isn't that useful for M6 anymore. The [precise](https://github.com/microprediction/precise) package is way more useful, and put one person on the podium! 

 # The book is on the way 
 You can [help me choose](https://www.linkedin.com/posts/petercotton_machinelearning-datascience-artificialintelligence-activity-6960853808872579072-SzDO?utm_source=linkedin_share&utm_medium=member_desktop_web)!
 
 The beginnings of a [book website](https://microprediction.github.io/building_an_open_ai_network/) includes [issues](https://github.com/microprediction/building_an_open_ai_network/issues) allowing you to complain about bugs. 
 
 ![](https://github.com/microprediction/home/blob/main/books/cover_choices.png)


