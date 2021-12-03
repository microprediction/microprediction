# PGA Tour Streams

The goal is provision of probabilistic estimates of scores that will be obtained on given holes. These streams are 
more about the course than the players, but of course the player ability enters the picture. 

### Hole difficulty streams 

As each golfer finishes player a hole, his score on that hole becomes the next data point in the series.

| Stream                                                                                         |  Typical values        |  Interpretation |
| ---------------------------------------------------------------------------------------------- | -------------------|-----------------------|
| [tour_1](https://www.microprediction.org/stream_dashboard.html?stream=tour_1)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 1st hole |
| [tour_2](https://www.microprediction.org/stream_dashboard.html?stream=tour_2)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 2nd hole |
| [tour_3](https://www.microprediction.org/stream_dashboard.html?stream=tour_3)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 3rd hole |
| [tour_4](https://www.microprediction.org/stream_dashboard.html?stream=tour_4)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 4th hole |
| [tour_5](https://www.microprediction.org/stream_dashboard.html?stream=tour_5)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 5th hole |
| [tour_6](https://www.microprediction.org/stream_dashboard.html?stream=tour_6)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 6th hole |
| [tour_7](https://www.microprediction.org/stream_dashboard.html?stream=tour_7)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 7th hole |
| [tour_8](https://www.microprediction.org/stream_dashboard.html?stream=tour_8)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 8th hole |
| [tour_9](https://www.microprediction.org/stream_dashboard.html?stream=tour_9)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 9th hole |
| [tour_10](https://www.microprediction.org/stream_dashboard.html?stream=tour_10)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 10th hole |
| [tour_11](https://www.microprediction.org/stream_dashboard.html?stream=tour_11)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 11th hole |
| [tour_12](https://www.microprediction.org/stream_dashboard.html?stream=tour_12)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 12th hole |
| [tour_13](https://www.microprediction.org/stream_dashboard.html?stream=tour_13)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 13th hole |
| [tour_14](https://www.microprediction.org/stream_dashboard.html?stream=tour_14)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 14th hole |
| [tour_15](https://www.microprediction.org/stream_dashboard.html?stream=tour_15)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 15th hole |
| [tour_16](https://www.microprediction.org/stream_dashboard.html?stream=tour_16)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 16th hole |
| [tour_17](https://www.microprediction.org/stream_dashboard.html?stream=tour_17)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 17th hole |
| [tour_18](https://www.microprediction.org/stream_dashboard.html?stream=tour_18)  |  -2, -1, 0, 1, 2, 3, 4 ...    |  Score on 18th hole |

Values have the usual interpretation relative to par:

| Value                                                                                         |  Interpretation       |  
| ---------------------------------------------------------------------------------------------- | -------------------|
| -2 |  Eagle    |
| -1 |  Birdie    |
| 0 |  Par    |
| 1 |  Bogey    |
| 2 |  Double    |

and so on. 
 
### Exogenous factors
 
Factors influencing the difficulty of the hole, not yet provided, include distance and geometry of the hole, pin placement, 
speed of green, strength and direction of prevailing wind, and so forth. Pin placements vary round to round, yet performance of 
players on a given hole on previous days is still relevant. 


### Auxiliary streams: player ability breakdown

Long term mean ability of players who played the 9th hole but not yet the 10th hole:  

| Stream                                                                                         |  Breakdown         |  
| ---------------------------------------------------------------------------------------------- | -------------------|
| [tour_10_sg_app](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_sg_app)  |  Approach shots    |
| [tour_10_sg_ott](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_sg_ott)  |  Off the tee       |
| [tour_10_sg_arg](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_sg_arg)  |  Scrambling        |
| [tour_10_sg_putt](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_sg_arg)  |  Putting        |
| [tour_10_sg_total](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_sg_arg)  |  Total           |

The tournament performance for the same players:

| Stream                                                                                         |  Breakdown         |  
| ---------------------------------------------------------------------------------------------- | -------------------|
| [tour_10_tourn_app](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_tourn_app)  |  Approach shots    |
| [tour_10_tourn_ott](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_tourn_ott)  |  Off the tee       |
| [tour_10_tourn_arg](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_tourn_arg)  |  Scrambling        |
| [tour_10_tourn_putt](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_tourn_putt)  |  Putting        |
| [tour_10_tourn_t2g](https://www.microprediction.org/stream_dashboard.html?stream=tour_10_tourn_t2g)  |  Total           |


### Auxiliary streams: hole score streams broken down by player ability category 

There are also streams which report hole performance only for players whose overall ability falls into one of four categories. For
example a score is reported in at most one of the following streams when a player completes the 17th hole: 

| Stream    |   Player categorization         | Long term player ability range | 
| ----------|-------------------------------- | ----------------------------------------------| 
| [tour_17_great](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_great) | Great |  1.34 to 2.0 |
| [tour_17_good](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_good)  | Good  |   0.67 to 1.33 |
| [tour_17_okay](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_okay)  | Okay   |  -0.25 to 0.25 | 
| [tour_17_bad](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_bad) | Bad | -0.67 to -1.33 | 

Note that these are not exhaustive, so sometimes these streams will not tick if a player is not close to 1.67, 1, 0 or -1. 

See [Defassa Dog](https://github.com/microprediction/microprediction/tree/master/submission_examples_golf) for an example of a prediction that 
utilizes these streams to provide predictions of [tour_17](https://www.microprediction.org/stream_dashboard.html?stream=tour_17). 
