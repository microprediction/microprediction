import math
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import os
import json
from getjson import getjson
from microprediction.whereami import TOP
from microprediction.live.iex import iex_common_stock_with_balance_sheet_tickers


XRAY_TICKERS_JSON = os.path.join(TOP,'live', 'xraytickers.json')
XRAY_TICKERS_REVERSE_JSON = os.path.join(TOP ,'live' ,'xraytickersreverse.json')

STOCK_THRESHOLD = 250*1000*1000*1000

HARDWIRED_TICKERS=['aapl','abbv','abt','acn','adbe',
                   'aig','amd','amgn','amt','amzn',
                   'avgo','axp','ba','bac','bk','blk',
                   'bmy','brk.b','c','cat','chtr','cl',
                   'cmcsa','cof','cop','cost','crm','csco',
                   'cvs','dhr','dis','dow','duk','emr',
                   'exc','f','fdx','gd','ge',
                   'gild','gm','goog','googl','gs',
                   'hd','hon','ibm','intc','jnj','jpm',
                   'khc','ko','lin','lly','lmt','low',
                   'ma','mcd','mdlz','mdt','met','meta',
                   'mmm','mo','mrk','ms','msft','nee',
                   'nflx','nke','nvda','orcl','pep',
                   'pfe','pg','pm','pypl','qcom','rtx',
                   'sbux','schw','so','spg','t','tgt',
                   'tmo','tmus','tsla','txn','unh',
                   'unp','ups','usb','v','vz','wba',
                   'wfc','wmt','xom']


def reasonable_threshold():
    # Get common stock value for VSAT, the smallest company in Russell 1000
    from microprediction.live.iexcredentials import get_iex_key
    tickers = ['vsat']
    common = iex_common_stock_with_balance_sheet_tickers(api_key=get_iex_key(), return_tickers=False, tickers=tickers)
    print(common)
    return common


def create_xray_tickers_json():
    """
       Create JSON file storing "official" list of tickers using in the x-ray experiment
    """
    tickers = iex_common_stock_with_balance_sheet_tickers(api_key=IEX_KEY, return_tickers=True, threshold=STOCK_THRESHOLD)
    save_tickers(tickers=tickers )


def save_tickers(tickers):
    tickers_dict = dict([(k, ticker) for k, ticker in enumerate(tickers)])
    with open(XRAY_TICKERS_JSON, 'wt') as fp:
        json.dump(obj=tickers_dict, fp=fp)
    tickers_reverse_dict = dict(sorted([(ticker, k) for k, ticker in enumerate(tickers)]))
    with open(XRAY_TICKERS_REVERSE_JSON, 'wt') as fp:
        json.dump(obj=tickers_reverse_dict, fp=fp)


def cull_xray_tickers_json(new_threshold):
    """
       Create JSON file storing "official" list of tickers using in the x-ray experiment
    """
    all_tickers = HARDWIRED_TICKERS
    tickers = iex_common_stock_with_balance_sheet_tickers(api_key=IEX_KEY, tickers=all_tickers, return_tickers=True,threshold=new_threshold)
    save_tickers(tickers=tickers)


def get_xray_tickers() -> [str]:
    """ Retrieve xray tickers """
    url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json'
    data = getjson(url, failover_url=url)
    return [data[str(i)] for i in range(len(data))]


def get_yarx_generic_names():
    return [ 'yarx_'+ticker.replace('.','-')+'.json' for ticker in get_xray_tickers() ]


def get_quick_yarx_names():
    return [name.replace('yarx','quick_yarx') for name in get_yarx_generic_names()]


def get_middling_yarx_names():
    return [ 'middling_yarx_'+ticker+'.json' for ticker in get_xray_tickers() ]


def get_slow_yarx_stream_names():
    return [ 'slow_yarx_'+ticker+'.json' for ticker in get_xray_tickers() ]




if __name__ == '__main__':
    tickers = get_xray_tickers()
    print('There are '+str(len(tickers))+' on github JSON ')
    CULL_TICKERS = False
    if CULL_TICKERS:
        from microprediction.live.iexcredentials import get_iex_key
        IEX_KEY = get_iex_key()
        cull_xray_tickers_json()
    else:
        print(reasonable_threshold())
        from microprediction.live.iexcredentials import get_iex_key
        IEX_KEY = get_iex_key()
        cull_xray_tickers_json(new_threshold=STOCK_THRESHOLD*1)
