## Copulas

If you are familiar with how to [predict](https://microprediction.github.io/microprediction/predict.html) and
you have noticed the [zstreams](https://microprediction.github.io/microprediction/zstreams.html) that are created, you
might consider some more advanced functionality. The /copula API serves two purposes:

 - Simultaneous publication of multiple streams
 - Simultaneous publication of multiple streams with associated z2 or z3 `copula' streams 

The following family of streams illustrates the pattern.
         
|  Functionality          |  Example dashboard URL                                                            |
|-------------------------|-----------------------------------------------------------------------------------|
|  Base stream #1         |  `https://www.microprediction.org/stream_dashboard.html?stream=c5_iota`               |
|  Base stream #2         |  `https://www.microprediction.org/stream_dashboard.html?stream=c5_bitcoin`               |
|  Z-scores               |  `https://www.microprediction.org/stream_dashboard.html?stream=z1~c5_iota~310`        |
|  Bivariate copula       |  `https://www.microprediction.org/stream_dashboard.html?stream=z2~c5_iota~pe~910`     |
|  Trivariate copula      |  `https://www.microprediction.org/stream_dashboard.html?stream=z3~c5_iota~c5_bitcoin~pe~910` |         
TODO: verify links

To reiterate there are NO MULTIVARIATE streams on microprediction.org. However there are
univariate streams whose values represent a point in R^2 or R^3. The mapping from one dimension to 
two or three is implied. The former is used by streams prefixed by z2~, the latter by streams prefixed by
z3~. For this purpose Morton space filling Z-curves are employed. The most up to date
reference for these embeddings is the code (see [zcurve_conventions](https://github.com/microprediction/microconventions/blob/master/microconventions/zcurve_conventions.py) ). There is

### Python 
Very similar to the use of set()

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='YOUR WRITE KEY HERE')
    names = ['my_stream_a.json','my_stream_b.json','my_stream_c.json', 'my_stream_d.json']
    values = [5,6,4,9]
    res = mw.cset(names=names,values=values)



 
