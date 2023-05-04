## Publishing a stream

Everyone is [doing it](https://www.linkedin.com/posts/thomashthoresen_datascience-microprediction-timeseriesforecasting-activity-6999971006274514944-lDID?utm_source=share&utm_medium=member_desktop). Here's how you can add to the list of [streams](https://www.microprediction.org/browse_streams.html). 



## 1. [Python](https://microprediction.github.io/microprediction/publish-using-python.html)

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')
    mw.set(name='my_stream.json',value=3.14157) 
    
See [publish-using-python](https://microprediction.github.io/microprediction/publish-using-python.html) for more utilities and patterns. 

## 2. R 

    library(httr)
    httr::PUT(url = paste0("https://api.microprediction.org/live/", 'my_stream.json'),
                  body = list(write_key = 'YOUR WRITE KEY HERE', budget = 1, value = 3.1457))
       
See Fred Viole's [r_examples](https://github.com/microprediction/microprediction/tree/master/r_examples). 

## 3. Julia 

    r = HTTP.request("PUT", "https://api.microprediction.org/live/my_stream.json";
    query=Dict(
        "write_key" => 'YOUR WRITE KEY',
        value => 3.14157))
    JSON.parse(String(r.body))
    
This example is from [Rusty Conover's Julia Client](https://github.com/rustyconover/Microprediction/blob/master/src/Microprediction.jl).

    
## 4. API 

Send a PUT request to [https://api.microprediction.org/live/my_stream.json](https://api.microprediction.org/live/my_stream.json) with the following parameters in the payload:

   - write_key
   - budget (can just set to 1)
   - value (e.g. 3.14157)


## Before you publish
Get your [writekey](https://microprediction.github.io/microprediction/writekeys.html) of difficulty 12 at least,
and learn about [bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html).


## After you publish

- Be patient, keep publishing, and promote your stream. 
- [Retrieve](https://microprediction.github.io/microprediction/retrieve.html) predictions.  
- View [zscores](https://microprediction.github.io/microprediction/zscores.html) to assess market efficiency.  



-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)

[Edit](https://github.com/microprediction/microprediction/blob/master/docs/publish.md) this page. 

![hallgrimshkirkja](https://github.com/microprediction/microprediction/blob/master/docs/assets/images/Hallgrimskirkja.png)
