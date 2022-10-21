
## Submitting predictions 

Conceptually speaking, to "predict" is to supply the following:

 - A list of *225* float 
 - A delay, which must be 70, 310, 910 or 3555 seconds. 
 - A stream name.  

The goal is to have as many guesses as possible close in value to the 'ground truth'. The ground truth is 
the first number published after the delay has elapsed. 


### [Python](https://microprediction.github.io/microprediction/predict-using-python.html)

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')
    values = list(range(225))
    mw.submit(name='sombody_else_stream.json',delay=910, values=values)

This example is largely inadequate as it is not informed by
the history of the stream in question. See [predict-using-python](https://microprediction.github.io/microprediction/predict-using-python.html) for typical patterns.  

### R 
Following [r_examples](https://github.com/microprediction/microprediction/tree/master/r_examples)...

    name <- "z2~c5_iota~c5_ripple~3555.json"
    lagged <- jsonlite::fromJSON(paste0("https://api.microprediction.org/lagged/",name))
    x <- lagged[, 2, drop=FALSE]
    y <- c(x[1:50], x[1:200], x) 
    n <- 225
    probs <- seq(1/(2*n), 1-1/(2*n), length.out = n)
    q <- quantile(y, probs = probs, names=FALSE)
    my_values <- toString(q) 
    res <- httr::PUT(url = paste0("https://api.microprediction.org/submit/", name),
                 body = list(write_key = 'YOUR WRITE KEY HERE', delay=70, values = my_values))


### API
As suggested by the R example above, send PUT to https://api.microprediction.org/submit/die.json say, with payload:

    - write_key
    - delay
    - values (as a string with comma-separated values)


### The 8th rule of algo fight club is ...
... if this is your first visit you have to fight. If you have a spare bash shell:

         /bin/bash -c "$(curl -fsSL https://tinyurl.com/32jjebu9)"

This will install the needed packages into a virtual environment, burn a new write key, and then run the default crawler. It will then guide you
to relevant documentation, and to your dashboard. 


### Prerequisites
Get your [WRITE_KEY](https://microprediction.github.io/microprediction/writekeys.html) and scan
the [bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html) rules.


-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)

![norton](/microprediction/assets/images/norton.jpeg)


