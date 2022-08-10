## Submitting copula forecasts

Some streams, namely those with z2~ and z3~ prefixes, are best thought of as bivariate or trivariate (respectively) even though mechanically they are, as with all streams, univariate. This finesse is discussed in [copulas](https://microprediction.github.io/microprediction/copulas.html) from the perspective of the creator of the streams. 

When it comes to predicting these streams, some conveniences are made available in the Python client so you don't need to 
explicitly worry about the conventions for squishing 2-dim or 3-dim sequences into 1-dim. 

The code for [comble mammal](https://github.com/microprediction/microprediction/blob/master/submission_examples_copulas/comble_mammal.py) might be worth a look. But regardlesss the pattern is a simple one and illustrated below for the 2-dim case. 

- Pull z2~ history as a collection of tuples using [MicroReader](https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py).get_lagged_zvalues()
- Do something clever to create 2d samples 
- Submit as a collection of tuples using [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py).submit_zvalues()

In code:

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
