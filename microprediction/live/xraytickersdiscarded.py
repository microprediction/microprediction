
import json
import os
from microprediction.live.xraytickers import XRAY_TICKERS_JSON
from microprediction.whereami import TOP
from getjson import getjson

XRAY_TICKERS_OLD_JSON = os.path.join(TOP,'live', 'xraytickers_old.json')
XRAY_TICKERS_DISCARDED_JSON = os.path.join(TOP,'live', 'xraytickers_discarded.json')


def get_xray_tickers_discarded() -> [str]:
    """ Retrieve discarded xray tickers """
    url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers_discarded.json'
    data = getjson(url, failover_url=url)
    return [data[str(i)] for i in range(len(data))]


if __name__=='__main__':

    with open(XRAY_TICKERS_OLD_JSON) as fh:
        old_tickers = json.load(fh)

    with open(XRAY_TICKERS_JSON) as fh:
        new_tickers = json.load(fh)

    discarded = [(k, v) for (k,v) in old_tickers.items() if k not in new_tickers]

    with open(XRAY_TICKERS_DISCARDED_JSON, 'wt') as fp:
        json.dump(obj=discarded, fp=fp)
