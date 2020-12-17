
# Univariate Distribution Utilities

In our context a DistributionMachine (abbreviated Dist in some derived classes) is a running estimate of a 
univariate distribution updated one data point at a time. It must possess and inv_cdf function that takes (0,1)->R

### DistributionMachine

Examples of usage: 

- [statesboy cat](https://github.com/microprediction/microprediction/blob/master/crawler_examples/statesboy_cat.py)
- [thallodal cat](https://github.com/microprediction/microprediction/blob/master/crawler_examples/thallodal_cat.py)       


See article https://www.linkedin.com/pulse/live-online-distribution-estimation-using-t-digests-peter-cotton-phd/




