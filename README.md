
# microprediction [tldr](https://microprediction.github.io/microprediction/tldr), [docs](https://microprediction.github.io/microprediction/), [client](https://github.com/microprediction/microprediction) and [live leaderboards](https://www.microprediction.org/leaderboard.html) ![deploy](https://github.com/microprediction/microprediction/workflows/deploy/badge.svg) 
Packages and a platform for effecting autonomous prediction using lightweight markets instead of models because:
 
 - Markets are better at prediction than models - just harder to create and wield, until now.
 - Small "microprediction" ([glossary](https://microprediction.github.io/microprediction/glossary)) markets are surprisingly accurate too, and even [chatGPT can create one](https://medium.com/geekculture/chatgpt-acquires-realtime-operational-intelligence-23675d2e0f3b).

See [tldr](https://microprediction.github.io/microprediction/tldr) or just [instantly participate](https://microprediction.github.io/microprediction/setup) and you'll grok it, I promise.  
### Provocations (more in the [book](https://mitpress.mit.edu/books/microprediction))

- A market beat 97% of participants in the M6 contest([post](https://www.linkedin.com/posts/petercotton_the-options-market-beat-94-of-participants-activity-7020917422085795840-Pox0?utm_source=share&utm_medium=member_desktop)) and [announcement](https://www.linkedin.com/posts/spyros-makridakis-b2ba5a52_congratulations-to-the-global-winners-of-activity-7028775981133791232-Mlzs?utm_source=share&utm_medium=member_desktop). 
- No timeseries model should ever be called SOTA again. [Discuss](https://www.linkedin.com/posts/petercotton_timeseries-forecasting-timeseriesanalysis-activity-6987561356862353408-iy2Z?utm_source=share&utm_medium=member_desktop) and disagree but your argument [probably reduces to a contradiction](https://github.com/microprediction/building_an_open_ai_network/discussions/19).   
- Modeling [is central planning](https://www.linkedin.com/posts/petercotton_feedback-activity-7029452936686489600-8iuX?utm_source=share&utm_medium=member_desktop), a fatal conceit. Why limit capabilities to a single mind, algorithm or company? 
- Somebody's algorithm or data will find signal in your model residuals, someday ([instructions](https://microprediction.github.io/microprediction/residuals)).
- Most of "AI" will be done analogously, eventually, though this will take work. See the [book](https://mitpress.mit.edu/books/microprediction) or [challenge me](https://github.com/microprediction/building_an_open_ai_network/discussions).

 
 ![](https://github.com/microprediction/microprediction/blob/master/docs/assets/images/cotton_microprediction_3d_down.png)

## Try it out ([docs](https://microprediction.github.io/microprediction/), [install](https://github.com/microprediction/microprediction/blob/master/INSTALL.md) and live [help](https://microprediction.github.io/microprediction/meet.html))

If you would like to see how *easy* it is to wield a *new kind of market* to effect turnkey distributional prediction, see the [docs](https://microprediction.github.io/microprediction/) and, therein, observe that you can receive live [help](https://microprediction.github.io/microprediction/meet.html) getting started on Fridays, or in the [slack channel](https://microprediction.github.io/microprediction/slack.html). Key points:

 - No barriers to entry. To predict, just open this [notebook](https://github.com/microprediction/microprediction/blob/master/notebook_examples_submission/enter_microprediction_contest.ipynb) and run it, or cut and paste a [one line bash command](https://microprediction.github.io/microprediction/setup). 
 - The microprediction platform makes it [pretty trivial](https://microprediction.github.io/microprediction/publish.html) to initiate your own bespoke market too. Just ask Thomas Hjelde Thorensen who recently [posted](https://www.linkedin.com/posts/thomashthoresen_datascience-microprediction-timeseriesforecasting-activity-6999971006274514944-lDID?utm_source=share&utm_medium=member_desktop) about his experience. 
 - [Many algorithms](https://www.microprediction.org/leaderboard.html) already competing to predict [other streams](https://www.microprediction.org/browse_streams.html) can easily predict yours too. 
 - Many more will do so in the future. Anyone can [launch a new algorithm](https://microprediction.github.io/microprediction/predict.html) using anything they like in the Julia, R or Python [ecosystem](https://www.microprediction.com/blog/popular-timeseries-packages) for example (it's a data interface). 


Too hard? If you have a CSV with historical data (one column per variable) you can just send it to me (chat in [slack](https://microprediction.github.io/microprediction/slack.html) say). You can also just grab data, see the [reader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py).    

# The [TimeMachines](https://github.com/microprediction/timemachines), [Precise](https://github.com/microprediction/precise), and [HumpDay](https://github.com/microprediction/humpday) packages 

I also maintain three benchmarking packages to help me, and maybe you, surf the open-source wave. 

| Topic                  | Package           | Elo ratings | Methods                                                                                                                                                                                  | Data sources | 
|------------------------|-------------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------| 
| Univariate time-series | [timemachines](https://github.com/microprediction/timemachines)  | [Timeseries Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_003.html) | Most popular packages ([list](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters))                                                                           | [microprediction streams](https://www.microprediction.org/browse_streams.html)                                      |
| Global derivative-free optimization | [humpday](https://github.com/microprediction/humpday) |  [Optimizer Elo ratings](https://microprediction.github.io/optimizer-elo-ratings/html_leaderboards/overall.html) | Most popular packages ([list](https://github.com/microprediction/humpday/tree/main/humpday/optimizers))                                                                                  | A mix of classic and new [objectives](https://github.com/microprediction/humpday/tree/main/humpday/objectives)      |
| Covariance, precision, correlation | [precise](https://github.com/microprediction/precise) | See [notebooks](https://github.com/microprediction/precise/tree/main/examples_colab_notebooks) | [cov](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md) and [portfolio](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md) lists |Stocks, electricity etc                                                                                              | 

These packages aspire to advance online autonomous prediction in a small way, but also help me notice if anyone else does.  

### How [microprediction.org](https://www.microprediction.org/browse_streams.html) "house" algorithms use these packages
Advances in time-series prediction funnel down into microprediction algorithms in various ways:

1. The "[/skaters](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters)" provide canonical, single-line of code access to functionality drawn from packages like [river](https://github.com/online-ml/river), [pydlm](https://github.com/wwrechard/pydlm), [tbats](https://github.com/intive-DataScience/tbats), [pmdarima](http://alkaline-ml.com/pmdarima/), [statsmodels.tsa](https://www.statsmodels.org/stable/tsa.html), [neuralprophet](https://neuralprophet.com/), Facebook [Prophet](https://facebook.github.io/prophet/), 
   Uber's [orbit](https://eng.uber.com/orbit/), Facebook's [greykite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library) and more. 
   
2. The [StreamSkater](https://microprediction.github.io/microprediction/predict-using-python-streamskater.html) makes it easy to use any "skater". 

3. Choices are sometimes advised by [Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_003.html), but anyone can do what they want. 

4. It's not too hard to use my [HumpDay](https://github.com/microprediction/humpday) package for offline meta-param tweaking, et cetera. 

5. It's not too hard to use my [precise](https://github.com/microprediction/precise) package for online ensembling. 

There are other ways. Look for CODE badges on [leaderboards](https://www.microprediction.org/leaderboard.html).  

### Some microprediction platform repos

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


# About me ([home](https://github.com/microprediction/home))
  - [blog](https://microprediction.medium.com)
  - [slack channel](https://microprediction.github.io/microprediction/slack.html) 
  - [office hours](https://microprediction.github.io/microprediction/meet.html)
  - [papers, articles etc](https://github.com/microprediction/home)

# Acknowledgements
The live microprediction platform is supported by [Intech Investments](https://www.intechinvestments.com/) and not, as rumoured, the [Center for Artificial Artificial Intelligence](https://microprediction.github.io/microprediction/aai). 
