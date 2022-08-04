## Submitting copula forecasts

As illustraed by [comble mammal](https://github.com/microprediction/microprediction/blob/master/submission_examples_copulas/comble_mammal.py) but
in this example we use some convenience methods to pull z2~ history as a collection of tuples, and also submit
a collection of tuples. The user of this pattern is not thinking about the 
details of the space-filling curves implicit in the [copulas](https://microprediction.github.io/microprediction/). 

Instead, we use the [MicroReader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py).get_lagged_zvalues() method
and the [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py).submit_zvalues()

     NAMES = [ n for n in mw.get_stream_names() if 'z2~' in n or 'z3~' in n ]
     for _ in range(10):
        name = random.choice(NAMES)
        for delay in mw.DELAYS:
            lagged_zvalues = mw.get_lagged_zvalues(name=name, count= 5000)
            if len(lagged_zvalues)>20:
                zvalues = fit_and_sample(lagged_zvalues=lagged_zvalues, num=mw.num_predictions)
                try:
                    res = mw.submit_zvalues(name=name, zvalues=zvalues, delay=delay )
                    pprint(res)
                except Exception as e:
                    print(e)
                time.sleep(1)

Of course, submit_zvalues() calls [MicroWriter.submit()](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py).


-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)
