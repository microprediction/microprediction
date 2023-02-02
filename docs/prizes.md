# Prizes


### Daily prize mechanism
A cash prize is awarded daily, as follows:

- Performance on streams is aggregated by sponsor
- A sponsor is chosen each day. The more important sponsors are chosen more often. 
- The importance of the sponsor is reflected in the prizemoney shown on the [leaderboards](https://www.microprediction.org/leaderboard.html) and [prize api](https://api.microprediction.org/prizes/) 
- Once a sponsor and type of contest is selected, the current leaderboard is polled. 
- A weight is assigned to each contestant proportional to (score-threshold) raised to an exponent. The threshold is set at a fraction of the best score. 
- The parameters may be tweaked from time to time. Transparency into parameters and selection probabilities is provided in the [slack](https://microprediction.github.io/microprediction/slack.html) in the microprediction-stream-notifications channel. 
- Over time, prizes awarded more or less reflect these weights. 
- The maintainer reserves all discretion 

To get prizes and sponsors from in Python I suggest:

    from getjson import getjson
    prizes = getjson('https://api.microprediction.org/prizes/')

### Rules, legalities and additional background information
Short version: you need to be in a country where Paypal operates. 

 - See [daily prize](https://www.microprediction.com/competitions/daily) on the .com informational site for advice, but be aware that the APIs provide the definitive numbers and sponsor lists.  
 - See the [full contest rules](https://www.microprediction.com/contest-rules). 



-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)

[Edit](https://github.com/microprediction/microprediction/blob/master/docs/prizes.md) this page. 
 
