## Z-scores and Z1~ streams

It is assumed here that you can [publish](https://microprediction.github.io/microprediction/publish.html) and have 
created a stream. You may have noticed that two z1~ streams were also created. To illustrate, in the case
of the 'die.json' stream we have the following:
 
| Type        | Example stream pages                                                                         |
|-------------|----------------------------------------------------------------------------------------------|
| Base stream | [die.json](https://www.microprediction.org/stream_dashboard.html?stream=die)                 |
| Z-scores    | [z1~die~70.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~70)     |
| Z-scores    | [z1~die~3555.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~3555) |

### Creating z1~ streams
There's nothing to do! Z1~ streams are created automatically 
when you [publish](https://microprediction.github.io/microprediction/publish.html) a regular stream. 


### The meaning of z1~ streams 

Using the example [z1~die~70.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~70) we assume
a new point $x$ is published. We also assume a mapping $F_{70}: x \rightarrow [0,1]$ that is implied by the
community predictions for $x$ pertaining to the $70$ second horizon. 



 
