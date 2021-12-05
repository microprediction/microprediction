from microprediction.bespoke.meme_stock import encode_meme_stock_old, decode_meme_stock_old, encode_meme_stock, decode_meme_stock


def test_encodings():
    assert (encode_meme_stock_old('GME') == 717769)
    assert (encode_meme_stock_old('TSLA') == 84837665)


def test_round_trip():
    for ticker in ['GME','ABAB','TSLA','LONGTICKER']:
        y = encode_meme_stock(ticker)
        assert ticker==decode_meme_stock(y)


if __name__=='__main__':
    print(test_round_trip())
    print((encode_meme_stock('CC')-encode_meme_stock_old('BB'))/1e-4)