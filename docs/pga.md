## PGA Tour streams

There are streams intended to provide a handle on the course:

| Shorthand             | Example                                                                                                | Description                                      |
|-------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| Scores by greats players   | [tour_11_great.json](https://www.microprediction.org/stream_dashboard.html?stream=tour_11_great)          | Next net hole score by a great player on hole 11     |
| Scores by good players  | [tour_18_good.json](https://www.microprediction.org/stream_dashboard.html?stream=tour_18_good)     | Next net hole score by any good player on hole 18|
| Scores by okay players   | [tour_17_okay.json](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_okay)      | Next net hole score by any okay player on hole 17 |
| Scores by bad players   | [tour_13_bad.json](https://www.microprediction.org/stream_dashboard.html?stream=tour_13_bad)      | Next net hole score by any bad player on hole 17 |
| Scores by any player   | [tour_7.json](https://www.microprediction.org/stream_dashboard.html?stream=tour_7)      | Next net hole score by any player on hole 7 |



### Definition of "good" etc

| Category | Skill Range                           | Description                                          |
|----------|---------------------------------------|------------------------------------------------------|
| great    | 1.34 ≤ skill ≤ 2.0                    | Player's skill is within 0.33 of 1.67                |
| good     | 0.67 ≤ skill ≤ 1.33                   | Player's skill is within 0.33 of 1.0                 |
| okay     | -0.25 ≤ skill ≤ 0.25                  | Player's skill is within 0.25 of 0.0                 |
| bad      | -1.33 ≤ skill ≤ -0.67                 | Player's skill is within 0.33 of -1.0                |


### Contender hole streams

There are also streams intended to serve as something better than a leaderboard. There are contender streams where the actual score by a particular player on a particular hole is published repeatedly when that truth is revealed. However prior to that, scores from other players playing the hole previously are also included. This is an experimental hybrid setup. 


| Shorthand             | Example                                                                                                | Description                                      |
|-------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| Player 1 hole 11   | [pga_contender_1_hole_11.json](https://www.microprediction.org/stream_dashboard.html?stream=pga_contender_1_hole_11)          | The score on hole 11 by the 2nd listed condender, but also other scores by other players on the same hole prior to that    |


See the updated contenders [names](https://micropredictionmiscstreams.pythonanywhere.com/contenders/names) and [scores](https://micropredictionmiscstreams.pythonanywhere.com/contenders/scores). For instance:

    from getjson import getjson
    contenders = getjson('https://micropredictionmiscstreams.pythonanywhere.com/contenders/name')

Also:

    def contender_stream_name(contender_ndx, hole):
         return 'pga_contender_'+str(contender_ndx)+'_hole_'+str(hole)+'.json'


### Approximate player skill (contenders only)

To get a rough idea of player ability:

   - [sg_total](https://micropredictionmiscstreams.pythonanywhere.com/contenders/form/sg_total)

for example:

    ability = getjson('https://micropredictionmiscstreams.pythonanywhere.com/contenders/form/sg_total')
   


-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)
 
  



