
## Z-scores and Z1~ streams

It is assumed here that you can [publish](https://microprediction.github.io/microprediction/publish.html) and have 
created a stream. You may have noticed that two z1~ streams were also created. To illustrate, in the case
of the 'die.json' stream we have the following:
 
| Type        | Example stream pages                                                                         | CDF used (the F)                                                                                              |
|-------------|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| Base stream | [rdps_xlp.json](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp)                 |                                                                                                               |
| Z-scores    | [z1\~rdps_xlp\~70.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~rdps_xlp~70)     | die.json [70 second horizon](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp&horizon=70)     |
| Z-scores    | [z1\~rdps_xlp\~3555.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~rdps_xlp~3555)     | die.json [3555 second horizon](https://www.microprediction.org/stream_dashboard.html?stream=rdps_xlp&horizon=3555)     |


### Creating z1~ streams
Nothing to do. 

The z1~ streams are created automatically 
when you [publish](https://microprediction.github.io/microprediction/publish.html) a regular stream. 


### The meaning of z1~ streams 

Using the example [z1~die~70.json](https://www.microprediction.org/stream_dashboard.html?stream=z1~die~70) we assume
a new point \(x\) is published. We also assume a mapping: 

$$ F_{70}: x \rightarrow [0,1] $$

that is the distributional transform implied by (most of the) community predictions for $x$ pertaining to the $70$ second horizon. 
Here I skip over some engineering nuances, to be honest, but assuming
the `community distributional transform` is thus defined, the 'z-score' is given by

$$ z_1 = \Phi^{-1}\left( F_{70}(x)  \right) $$

where $\Phi$ is the standard normal distribution function. 

### Approximate standard normality of z1~ streams

If the competition to predict the parent stream is intense, it stands to reason that $p=F_{70}(x)$ is approximately 
uniform and therefore 'z' values reported in z1~ streams are approximately $N(0,1)$. 

Indeed there are several 
algorithms whose only purpose in life is making $N(0,1)$-inspired predictions of z1~ streams. However, your algorithm might notice departure from standard normality and profit from the same. 


### Feeling fancy?
See [copulas](https://microprediction.github.io/microprediction/copulas.html) for 
an extension of the community zscore idea to two and three dimensions. 

-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)
