Your options for publishing a data point:

## 1. Python client 

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')
    mw.set(name='my_stream.json',value=3.14157) 

## 2. R 
There is no official R client, but you can do this:

    library(httr)
    httr::PUT(url = paste0("https://api.microprediction.org/live/", 'my_stream.json'),
                  body = list(write_key = 'YOUR WRITE KEY HERE', budget = 1, value = 3.1457))
       
See [r_examples](https://github.com/microprediction/microprediction/tree/master/r_examples). 

## 3. Julia 
I suggest using or modifying [Rusty Conover's Julia Client](https://github.com/rustyconover/Microprediction/blob/master/src/Microprediction.jl). e.g.:

    r = HTTP.request("PUT", "https://api.microprediction.org/live/my_stream.json";
    query=Dict(
        "write_key" => 'YOUR WRITE KEY',
        value => 3.14157))
    JSON.parse(String(r.body))
    
## 4. API 

