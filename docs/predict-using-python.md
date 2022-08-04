## Submitting predictions using python
Usually you'd use one of

      MicroWriter        (memoryless cron job, say)
          |
      MicroCrawler       (intended to be run as continuous process)

or a fancy descendent of MicroCrawler. 

### Option 1. BYO scheduling with MicroWriter
Use [MicroWriter](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py).submit() as illustratd by
[callable_flea.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_independent/callable_flea.py)

    NAMES = get_xray_stock_names() + XRAY_PORTFOLIO_NAMES
    from microprediction.live.xraytickers import get_xray_stock_names
    from microprediction.live.xrayportfolios import XRAY_PORTFOLIO_NAMES

    for name in NAMES:
        lagged_values = mw.get_lagged_values(name=name)
        padded = [-1, 0, 1 ] + list(lagged_values) + list(lagged_values[:5]) + list(lagged_values[:15])
        devo = np.std(padded)
        values = sorted( [ devo*mw.norminv(p) +  0.001 * np.random.randn() for p in mw.percentiles()] )
        nudged = StatsConventions.nudged(values)
        for delay in mw.DELAYS:
            mw.submit(name=name, values=values, delay=delay)
            time.sleep(1)  # <-- Out of consideration for the system

This might be run once an hour, or once a day say. 

### Option 2: [Use MicroCrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html).
Another pattern is:

  1. Subclass MicroCrawler
  2. Instantiate with your WRITE_KEY
  3. Call the run() method

This will create an algorithm that slowly explores the stream universe. You can override the
default prediction and navigation logic. See [predict-using-python-microcrawler](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html).


### Option 3: MicroWriter copula submission methods
Applicable only to copula streams. See [predict-using-python-copulas](https://microprediction.github.io/microprediction/predict-using-python-copulas.html).






-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)
