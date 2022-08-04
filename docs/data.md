Ways to retrieve data for research, or whatever. 

### CSV 
Links uch as [https://csv.microprediction.org/lagged?name=die.json](https://csv.microprediction.org/lagged?name=die.json) download
the recent history of die rolls (say).

### Python

    from microprediction import MicroReader
    mr = MicroReader()
    y = mr.get_lagged_values(name="faang_0.json")
    
For other possibilities, see the [MicroReader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py) client code. 

## R


    library(jsonlite)
    lagged <- jsonlite::fromJSON(paste0("https://api.microprediction.org/lagged/",name))
    x <- lagged[, 2, drop=FALSE]
   
   
See also [r_examples](https://github.com/microprediction/microprediction/tree/master/r_examples). 

### Julia

Use get_lagged from [julia client](https://github.com/rustyconover/Microprediction/blob/master/src/Microprediction.jl)

### API

GET [https://api.microprediction.org/lagged/die.json](https://api.microprediction.org/lagged/die.json)

Documentation [map](https://microprediction.github.io/microprediction/map.html)
  