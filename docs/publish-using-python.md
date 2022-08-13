More detail on publishing streams using Python. See [publish](https://microprediction.github.io/microprediction/publish) for alternatives. 

## Publishing using Python 

    pip install microprediction

### BYO scheduling
Just use [MicroWriter.set()](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) to publish. 

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')
    mw.set(name='my_stream.json',value=3.14157) 
    

### MicroPoll
Alternatively, use [MicroPoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) 
as illustrated by [traffic_speed.py](https://github.com/microprediction/microprediction/blob/master/stream_examples_traffic/traffic_speed.py).

    from microprediction.polling import MicroPoll
    from microprediction.live.nyc_traffic import verrazano_speed
    poller = MicroPoll(write_key='YOUR KEY HERE',
                         name='verrazano_speed.json',
                         func=verrazano_speed,
                         interval=15)
    poller.run()

Here interval is in minutes. The argument `func` should be a function returning
a float, and you can supply `func_args` if needed. 

### MicroChangePoll
It often pays to publish changes to live quantities, rather than absolute values, as this 
obviates the need for algorithms to precisely anticipate publishing times. 
The class [MicroChangePoll](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py) can
help and is illustrated by [traffic_speed_changes.py](https://github.com/microprediction/microprediction/blob/master/stream_examples_traffic/traffic_speed_changes.py). Note
the suspension and resumption logic. 

### MultiChangePoll
See [faang.py](https://github.com/microprediction/microprediction/blob/master/stream_examples_faang/faang.py) for an illustration
of using slightly more advanced functionality provided in
[polling.py](https://github.com/microprediction/microprediction/blob/master/microprediction/polling.py), including
the use of a `change_func` to create streams that are functionals of changes
in values. 




### After you publish

- Be patient, keep publishing, and promote your stream. 
- [Retrieve](https://microprediction.github.io/microprediction/retrieve.html) predictions.  
- View [zscores](https://microprediction.github.io/microprediction/zscores.html) to assess market efficiency.  

### Video tutorials 

- The ten minute data science project [vimeo](https://vimeo.com/443203883)
- [Creating a data stream](https://microprediction.github.io/microprediction/video-python-4.html)

-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)
