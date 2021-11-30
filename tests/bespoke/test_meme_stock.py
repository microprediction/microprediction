from microprediction.bespoke.meme_stock import encode_meme_stock, decode_meme_stock


def test_encodings():
    assert (encode_meme_stock('GME') == 717769)
    assert (encode_meme_stock('TSLA') == 84837665)