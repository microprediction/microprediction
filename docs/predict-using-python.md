## Submitting predictions using python
Usually you'd use one of

      MicroWriter        
          |
      MicroCrawler       

or perhaps a fancy descendant of MicroCrawler. We consider each in turn.

### Option 1. Use [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py).submit()
If you intend to periodically run a script (say with cron) or otherwise
manage periodic submissions, then you may only need the [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py).submit() method
to get the job done. This is illustratd by
[callable_flea.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_independent/callable_flea.py)

    from microprediction import MicroWriter
    from microprediction.live.xraytickers import get_xray_stock_names
    from microprediction.live.xrayportfolios import XRAY_PORTFOLIO_NAMES
    from microconventions import MicroConventions
    NAMES = get_xray_stock_names() + XRAY_PORTFOLIO_NAMES
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')

    for name in NAMES:
        lagged_values = mw.get_lagged_values(name=name)
        padded = [-1, 0, 1 ] + list(lagged_values) + list(lagged_values[:5]) + list(lagged_values[:15])
        devo = np.std(padded)
        values = sorted( [ devo*mw.norminv(p) +  0.001 * np.random.randn() for p in mw.percentiles()] )
        nudged = StatsConventions.nudged(values)
        for delay in mw.DELAYS:
            mw.submit(name=name, values=values, delay=delay)
            time.sleep(1)  # <-- Out of consideration for the system

This might be run once an hour, or once a day say. Naturally you'll want to replace
the dubious model above with your own statistical ingenuity. 

### Option 1a: MicroWriter copula submission
See [predict-using-python-copulas](https://microprediction.github.io/microprediction/predict-using-python-copulas.html).


### Option 2: Use [MicroCrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html).run()
As an alternative to scheduled predictions, you can use a single long running process. 

  1. Subclass MicroCrawler
  2. Instantiate with your WRITE_KEY
  3. Call the run() method

This will create an algorithm that slowly explores the stream universe. In the first step
you can override the default prediction and navigation logic. See [predict-using-python-microcrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html).

### Option 2a: Use a specialized version of MicroCrawler
See 
 - [FitCrawler](https://microprediction.github.io/microprediction/predict-using-python-fitcrawler.html)
 - [StreamSkater](https://microprediction.github.io/microprediction/predict-using-python-streamskater.html)

You can also hunt in the [repository](https://github.com/microprediction/microprediction/tree/master/microprediction).

### Reminder: write keys

You can use a [colab notebook](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) to burn a new WRITE_KEY. 


-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)
