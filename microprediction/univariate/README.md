
# Univariate Distribution Utilities

In our context a DistributionMachine (abbreviated Dist in some derived classes) is a running estimate of a 
univariate distribution updated one data point at a time. It must possess and inv_cdf function that takes (0,1)->R

### DistributionMachine in SequentialStreamCrawler 

Examples of usage: 

- https://github.com/microprediction/microprediction/blob/master/crawler_examples/statesboy_cat.py
- https://github.com/microprediction/microprediction/blob/master/crawler_examples/thallodal_cat.py       

See article https://www.linkedin.com/pulse/live-online-distribution-estimation-using-t-digests-peter-cotton-phd/




