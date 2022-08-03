After you [publish](https://microprediction.github.io/microprediction/publish.html) repeatedly for some time, you can retrieve predictions submitted by other people's algorithms. 


### Python 
To retrieve predictions for the 70 second horizon:

     from microprediction import MicroReader
     mw = MicroReader()
     pred = mw.get_predictions(write_key='YOUR WRITE KEY HERE', name='your_stream.json', delay=70, strip=True, consolidate=True)

The allowable delays are in mw.DELAYS property, if you forget them. 

### API

Send GET to a URL like [http://api.microprediction.org/predictions/your_stream.json](http://api.microprediction.org/predictions/your_stream.json) with the following in the payload:
     - delay
     - write_key 
     
     
