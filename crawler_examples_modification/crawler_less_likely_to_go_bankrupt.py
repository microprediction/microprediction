from microprediction import MicroCrawler


# If you are truly patient, this will create a default crawler with a lot of leeway
# However before starting to predict, it may spend a lot of time (days) creating a write key
# Be sure to save the write key!
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


if __name__=='__main__':
    mw = MicroCrawler(difficulty=13)
    mw.run()