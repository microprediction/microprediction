## Z-scores and Z1~ streams

It is assumed here that you can [publish](https://microprediction.github.io/microprediction/publish.html) and have 
created a stream. You may have noticed that two z1~ streams were also created. To illustrate, in the case
of the 'die.json' stream we have the following:
 
| Type        | Example stream pages                                                                         |
|-------------|----------------------------------------------------------------------------------------------|
| Base stream | [die.json](https://www.microprediction.org/stream_dashboard.html?stream=die)                 |
| Z-scores    | [z1~die~70.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~70)     |
| Z-scores    | [z1~die~3555.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~3555) |

### Python or API
There's nothing to do. Z1~ streams are automatic when you [publish](https://microprediction.github.io/microprediction/publish.html)

### Interpretation

To use the example [z1~die~70.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~70), we observe
that every time a new point `x` is published to the parent stream [die.json](https://www.microprediction.org/stream_dashboard.html?stream=die) the
following value `z` is computed:
 1.  $ p = F_{70}(x)$
 2.  

 
