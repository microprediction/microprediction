
### Submit API 

To "predict" is to do the following:

 - Submit a list of *225* float (ultimately via api.microprediction.org/submit)
 - Specify a delay, which must be 70, 310, 910 or 3555 seconds. 
 - Specify a stream name.  

The goal is to have as many guesses as possible close in value to the 'ground truth'. The ground truth is 
the first number published after the delay has elapsed. 


### [Python](https://microprediction.github.io/microprediction/predict-using-python.html)

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')
    values = list(range(225))
    mw.submit(name='sombody_else_stream.json',delay=910, values=values)

See [predict-using-python](https://microprediction.github.io/microprediction/predict-using-python.html) for patterns and more. 

### R 
Following [r_examples](https://github.com/microprediction/microprediction/tree/master/r_examples)...

    name = 'name <- "z2~c5_iota~c5_ripple~3555.json"
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



