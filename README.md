
# microprediction (c.f. [home page](https://github.com/microprediction/home))
My more useful Python packages:

| Site | Topic |
|---|---|
| [precise.microprediction.org](https://precise.microprediction.org) | Online (incremental) covariance and correlation estimators. Supports both sklearn and river-ml conventions. Treats arrival and departure of variables. |
| [allocation.microprediction.org](https://allocation.microprediction.org) | Online (incremental) portfolio methods. Classics and two novel approaches: Schur and Thurstone. Asset smoothness and trading costs. Entry and exit of assets.  |
| [schur.microprediction.org](http://schur.microprediction.org) | Schur portfolio literature. Schur provided the unification of hierarchical and optimisation-based portfolio construction via block-matrix inversion. Now part of [skfolio](https://skfolio.org/auto_examples/clustering/plot_6_schur.html) and [allocation.microprediction.org](https://allocation.microprediction.org) per the above.|
| [thurstone.microprediction.org](http://thurstone.microprediction.org) | I invented the fast ability transform that makes Thurstone Class V models practical. Use this package for multi-entrant contest probabilities and inverse calibration. This [picture](https://thurstone.microprediction.org/) beats my words. |
| [humpday.microprediction.org](http://humpday.microprediction.org) | All the greatest derivative-free (black box) optimization methods in one place in pure Python and Javascript with no package dependencies. Comparison tooling, claude [skill](https://github.com/microprediction/humpday/blob/main/SKILL.md) and [interactive demos](https://humpday.microprediction.org/applications/index.html). |
| [skaters.microprediction.org](http://skaters.microprediction.org) | Fast and surprisingly reliable online univariate time series algorithms providing distributional predictions. Zero dependencies, runs in Pyodide. |



Writing, papers, blogs, expository:

| Site | Content |
|---|---|
| [book.microprediction.org](http://book.microprediction.org) | *Microprediction* — the book on splintering data science into small algorithmic agents. (Audio book too) |
| [microprediction.medium.com](https://microprediction.medium.com/) | Blog. Portfolio construction, optimization, time series, quantitative finance etc |
| [microprediction/home](https://github.com/microprediction/home/) | Papers - and some short musings |

Mostly expository:

| Site | Content |
|---|---|
| [conformalprediction.net](https://conformalprediction.net) | There's a small theoretical contribution: a KL-divergence theorem explaining clearly the limitations of conformal prediction. See this [demo](https://conformalprediction.net/demos/13-coverage-score-plane.html) for example. |
| [firstdown.microprediction.org](https://firstdown.microprediction.org) | I've been trying to change NFL team's first down strategy for years, with little success. |

As an aside, if you were redirected from the minor-cult article *Is Facebook's Prophet the Time-Series Messiah or Just a Very Naughty Boy?*, it moved [here](https://medium.com/geekculture/is-facebooks-prophet-the-time-series-messiah-or-just-a-very-naughty-boy-8b71b136bc8c). 


### What's with the Microprediction nom-de plume? 

I'm a career quant, applied mathematician, open-source developer, entrepreneur and father of three girls. My interests include quantitative finance, collective intelligence, sports analytics and mathematics in general. GitHub decided this should be my home page. 

This repo used to be the client for a high velocity prediction market I wrote for Intech Investments. It collected a billion predictions. As noted above I also wrote a [book](https://mitpress.mit.edu/books/microprediction) predicting that data science would splinter into little agents. I've long been a believer in engineering pipelines that anyone else can improve without asking permission, and in the eventual inversion of control between humans and machine in the "microprediction domain" (frequently repeated quantitative tasks). With the arrival of LLMs I'm convinced this applies to judgemental prediction also. It seems I have more faith in small markets than most, noting the important caveat made clear in the Indispensable Markets Hypothesis  [paper](https://github.com/microprediction/home/blob/main/workingpapers/The_Indispensible_Markets_Hypothesis.pdf) that markets can be indispensible yet not perfectly efficient. 

The [book](https://book.microprediction.com) was a meditation on the power of mini-markets and algorithmic statistical agents - a thesis that went from unlikely to almost self-evident as LLMs arrived. It predates phrases like "DeAI" and "Info Finance" (Buterin) not to mention the general explosion of interest in prediction markets ... but despite this shift in the zietgeist the ideas have a long way to go as far as seeping into general software engineering consciousness in concerned (judging by [this market](https://manifold.markets/MicropredictionnEzNp/prediction-markets-advocated-as-sys) anyway). 

![](https://github.com/microprediction/microprediction/blob/master/docs/assets/images/cotton_microprediction_3d_down.png)


## Rats and mice

- [manifoldbot](https://github.com/microprediction/manifoldbot) - A bot that uses LLMs to trade on manifold prediction markets. 
- [randomcov](https://github.com/microprediction/randomcov) - A set of quirky correlation and covariance matrix generators (I'd love your ideas). 
- [embarrassingly](https://github.com/microprediction/embarrassingly) - A speculative approach to robust optimization that sends impure objective functions to optimizers.
- [pandemic](https://github.com/microprediction/pandemic) - Ornstein-Uhlenbeck epidemic simulation (related [paper](https://arxiv.org/abs/2005.10311))
- [momentum](https://github.com/microprediction/momentum) - My most personally re-used mini package ... for incremental mean, var, skew, kurtosis.
- [muid](https://github.com/microprediction/muid) - Memorable Unique Identifiers ... try to figure out how that can't be an oxymoron.
- [timeseries-notebooks](https://github.com/microprediction/timeseries-notebooks) - Lots of examples of using open source timeseries packages.
- [correlationbounds](https://github.com/microprediction/correlationbounds) - Mini package for conf bounds
- [building_an_open_ai_network](https://github.com/microprediction/building_an_open_ai_network) - Book related.
- [recalibrate](https://github.com/microprediction/recalibrate) - Utils related to Platt scaling etc. 


  ![](https://github.com/microprediction/firstdown/blob/main/images/firstdownpaper.png)





