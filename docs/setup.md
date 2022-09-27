

## Setup
Sorry this won't work for windows folks but for everyone else, you can merely cut and paste into a terminal the following command.  

     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/microprediction/master/shell_examples/setup.sh)"
     
It would be prudent to first [read](https://raw.githubusercontent.com/microprediction/microprediction/master/shell_examples/run_default_crawler_forever.sh) what it will do. It will:

1. Create a crawling_working_dir
2. Create and activate a virtual python environment
3. Install the microprediction client
4. Burn a new private identity for you and save it to WRITE_KEY.txt (this takes a long time, sorry)
5. Instantiate a [MicroCrawler](https://github.com/microprediction/microprediction/blob/master/microprediction/crawler.py) which is an algorithm chauffeur. 
6. Run the crawler 
7. Invite you to cut and paste your writekey into the dashboard [dashboard](https://www.microprediction.org/) to see what [streams](https://www.microprediction.com/blog/livedata) it is predicting, and how well.    
8. Periodically bounce and upgrade.  

Once you are familiar with this process, you can return to the [crawler documentation](https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html) to see how to swap out the forecasting method for one that you invent, or simply prefer. You can also modify the navigation.  

-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)


![slack](/microprediction/assets/images/dashboard.png)


 
