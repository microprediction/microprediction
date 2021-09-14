from microprediction.simplecrawler import SimpleCrawler

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__ == "__main__":
    crawler = SimpleCrawler()
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.run()
