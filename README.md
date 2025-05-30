
# microprediction (Peter's Repos)
If you were redirected from: *Is Facebook's Prophet the Time-Series Messiah or Just a Very Naughty Boy?*, here's the [article](https://medium.com/geekculture/is-facebooks-prophet-the-time-series-messiah-or-just-a-very-naughty-boy-8b71b136bc8c).

Otherwise hi

 - My home page page contains [papers, working papers, articles](https://github.com/microprediction/home).
 - My [thanks for reaching out](https://github.com/microprediction/monteprediction/blob/main/TFRO.md) page contains contact suggestions. 
 - Medium [blog](https://microprediction.medium.com/)
 - [Linked-In](https://www.linkedin.com/in/petercotton/) content.
 - Robust portfolio theory [reading list](https://github.com/microprediction/precise/blob/main/LITERATURE.md).

I'm a career quant, applied mathematician, open-source developer, entrepreneur and dad.  

### Interests

 - Portfolio and ensemble construction (e.g. [paper](https://github.com/microprediction/home/blob/main/workingpapers/Hierarchical_Minimum_Variance_Portfolios.pdf) and [blog](https://medium.com/geekculture/schur-complementary-portfolios-fix-hierarchical-risk-parity-28b0efa1f35f) where I unified the two sides of portfolio theory).  
 - OTC microstructure (my day job so not public .. but for older work see [this](https://github.com/microprediction/home/blob/main/presentations/trading_illiquid.pdf) or [that](https://github.com/microprediction/home/blob/main/presentations/who_ya_gonna_call.pdf) or [the other](https://github.com/microprediction/home/blob/main/presentations/Benchmark___as_presented_at_NYU_Tandon_2016%20(1).pdf)).
 - Thurstone models (contests, LLM samplers etc)
 - Derivative-free optimization
 - Time-series
 - Sports analytics
 - Collective Intelligence, Decentralized AI
 - LLM uses for alpha, code gen, prediction and instrumentation (e.g. [pi](https://pi.crunchdao.com/)).

### Microprediction

I wrote a book on what we might call the Strong [Indispensable Markets Hypothesis](https://github.com/microprediction/home/blob/main/workingpapers/The_Indispensible_Markets_Hypothesis.pdf), and to help it along in a small way I run contests like [mid-one](https://mid-one.crunchdao.com/) which you might want to check out too as there is a lot of prize-money. I like to provoke people into using market-inspired collective mechanisms for prediction. I used the options market to effortlessly beat 97% of participants in the year-long M6 contest - see the [post](https://www.linkedin.com/posts/petercotton_the-options-market-beat-94-of-participants-activity-7020917422085795840-Pox0?utm_source=share&utm_medium=member_desktop) or [article](https://medium.com/geekculture/the-options-market-beat-94-of-participants-in-the-m6-financial-forecasting-contest-fa4f47f57d33). My [book](https://mitpress.mit.edu/books/microprediction) is a meditation on the power of mini-markets and algorithmic micro-managers in a very specific yet ubiquitous domain: frequently repeated prediction. It predates and extends phrases like "DeAI" and "Info Finance" (Buterin). Read the [awards and reviews](https://microprediction.github.io/building_an_open_ai_network/feedback.html). 

![](https://github.com/microprediction/microprediction/blob/master/docs/assets/images/cotton_microprediction_3d_down.png)

### Monteprediction 
Allow me to mention a long-running game where you hurl a million 11-dimensional Monte Carlo samples at my server. 

1. Open this [colab notebook](https://github.com/microprediction/monteprediction_colab_examples/blob/main/monteprediction_entry.ipynb) or [script](https://github.com/microprediction/monteprediction_colab_examples/blob/main/monteprediction_entry.py)  (yes there's an [R version](https://github.com/microprediction/monteprediction_colab_examples/blob/main/monteprediction_entry_rlang.ipynb)), 
2. Change the email, at minimum,
3. Run it. Every weekend.
4. Check your scores at [www.monteprediction.com](https://www.monteprediction.com)

The notebook also describes the scoring mechanism. Ask questions in the slack (see bottom of [leaderboard](https://www.monteprediction.com) for slack invite).

Now, here's some attempt to introduce you to my open source work ...

### Derivative-free optimizer comparisons

The [humpDay](https://github.com/microprediction/humpday) package is intended to help you choose a derivative-free optimizer for your use case. 

![](https://i.imgur.com/FCiSrMQ.png)

### Schur Complementary Portfolios

My work on unifying Hierarchical Risk Parity with minimum variance portfolio optimization sits in the [precise](https://github.com/microprediction/precise) package. See [slides](https://github.com/microprediction/home/blob/main/presentations/Schur_Complementary_Portfolios_2025__slides_.pdf) from a recent talk. 

<a href="https://medium.com/geekculture/schur-complementary-portfolios-fix-hierarchical-risk-parity-28b0efa1f35f">
<img src="https://github.com/microprediction/precise/blob/main/docs/assets/images/schur_reaction.png" width="600"></a>

### Incremental time-series and benchmarking

The [timemachines](https://github.com/microprediction/timemachines) package enumerates online methods and makes some effort to evaluate univariate methods against the corpus of time-series drawn from the microprediction platform. It is an attempt to reduce everything to relatively pure functions:

$$
    f : (y_t, state; k) \mapsto ( [\hat{y}(t+1),\hat{y}(t+2),\dots,\hat{y}(t+k) ], [\sigma(t+1),\dots,\sigma(t+k)], posterior\ state))
$$

where $\sigma(t+l)$ estimates the standard error of the prediction $\hat{y}(t+l)$. 


![](https://i.imgur.com/elu5muO.png)


### Benchmarking overview

| Topic                  | Package           | Elo ratings | Methods                                                                                                                                                                                  | Data sources | 
|------------------------|-------------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------| 
| Univariate time-series | [timemachines](https://github.com/microprediction/timemachines)  | [Timeseries Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/univariate-k_003.html) | Most popular packages ([list](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters))                                                                           | [microprediction streams](https://www.microprediction.org/browse_streams.html)                                      |
| Global derivative-free optimization | [humpday](https://github.com/microprediction/humpday) |  [Optimizer Elo ratings](https://microprediction.github.io/optimizer-elo-ratings/html_leaderboards/overall.html) | Most popular packages ([list](https://github.com/microprediction/humpday/tree/main/humpday/optimizers))                                                                                  | A mix of classic and new [objectives](https://github.com/microprediction/humpday/tree/main/humpday/objectives)      |
| Covariance, precision, correlation | [precise](https://github.com/microprediction/precise) | See [notebooks](https://github.com/microprediction/precise/tree/main/examples_colab_notebooks) | [cov](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md) and [portfolio](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md) lists |Stocks, electricity etc                                                                                              | 

These packages aspire to advance online autonomous prediction in a small way, but also help me notice if anyone else does.  

## Winning

The [winning](https://github.com/microprediction/winning) package includes my recently published fast algorithm for inferring relative ability from win probabilities, at any scale. As explained in the [paper](https://github.com/microprediction/winning/blob/main/docs/Horse_Race_Problem__SIAM_updated.pdf) the uses extend well beyond the pricing of quinellas! 

![](https://i.imgur.com/83iFzel.png) 

## First Down

My [firstdown](https://github.com/microprediction/firstdown) repo contains analysis aspiring to ruin great game of football. See Wilmott [paper](https://github.com/microprediction/firstdown/blob/main/wilmott_paper/44-49_Cotton_PDF5_Jan22%20(2).pdf) and for heaven's sake, don't stretch out for the first down. That's obviously nuts.  

  ![](https://github.com/microprediction/firstdown/blob/main/images/firstdownpaper.png)

## Some other repos

- [randomcov](https://github.com/microprediction/randomcov) - A set of quirky correlation and covariance matrix generators (I'd love your ideas). 
- [embarrassingly](https://github.com/microprediction/embarrassingly) - A speculative approach to robust optimization that sends impure objective functions to optimizers.
- [pandemic](https://github.com/microprediction/pandemic) - Ornstein-Uhlenbeck epidemic simulation (related [paper](https://arxiv.org/abs/2005.10311))
- [momentum](https://github.com/microprediction/momentum) - My most personally re-used mini package ... for incremental mean, var, skew, kurtosis.
- [muid](https://github.com/microprediction/muid) - Memorable Unique Identifiers ... try to figure out how that can't be an oxymoron.
- [timeseries-notebooks](https://github.com/microprediction/timeseries-notebooks) - Lots of examples of using open source timeseries packages.
- [correlationbounds](https://github.com/microprediction/correlationbounds) - Mini package for conf bounds
- [building_an_open_ai_network](https://github.com/microprediction/building_an_open_ai_network) - Book related.
- [recalibrate](https://github.com/microprediction/recalibrate) - Utils related to Platt scaling etc. 
  
## The currently defunct real-time time-series platform

The real-time system previously maintained by yours truly has entered a trisoloran dehydrated state but will hopefully be revived at a future date, after one of my three hundred ChatGPT generated scientific grant proposals is successful. Here's how some of the open-source stuff used to propagate down into the "algo fight club". 

1. The "[/skaters](https://github.com/microprediction/timemachines/tree/main/timemachines/skaters)" provide canonical, single-line of code access to functionality drawn from packages like [river](https://github.com/online-ml/river), [pydlm](https://github.com/wwrechard/pydlm), [tbats](https://github.com/intive-DataScience/tbats), [pmdarima](http://alkaline-ml.com/pmdarima/), [statsmodels.tsa](https://www.statsmodels.org/stable/tsa.html), [neuralprophet](https://neuralprophet.com/), Facebook [Prophet](https://facebook.github.io/prophet/), 
   Uber's [orbit](https://eng.uber.com/orbit/), Facebook's [greykite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library) and more. 
   
2. The [StreamSkater](https://microprediction.github.io/microprediction/predict-using-python-streamskater.html) makes it easy to use any "skater". 

3. Choices are sometimes advised by [Elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_003.html), but anyone can do what they want. 

4. It's not too hard to use my [HumpDay](https://github.com/microprediction/humpday) package for offline meta-param tweaking, et cetera. 

5. It's not too hard to use my [precise](https://github.com/microprediction/precise) package for online ensembling. 

A few repos that drove this:

- The [muid](https://github.com/microprediction/muid) identifier package is explained in this [video](https://vimeo.com/397352413). 
- [microconventions](https://github.com/microprediction/microconventions) captures things common to client and server, and may answer many of your more specific questions about prediction horizons, et cetera.  
- [rediz](https://github.com/microprediction/rediz) contains server side code. For the brave. 
- There are other rats and mice like [getjson](https://github.com/microprediction/getjson), [runthis](https://github.com/microprediction/runthis) and [momentum](https://github.com/microprediction/momentum).  



