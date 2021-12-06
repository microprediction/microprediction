from re import findall
from functools import reduce
import math

# Utilities for the Meme stock of the hour streams


def decode_meme_stock_old(encoded):
    """Decode an integer to a ticker."""
    return str(reduce(lambda x,y:x+y,map(
        lambda x:chr(int(x)),findall(r"[0-9][0-9]",
        str(int(encoded))))))


def encode_meme_stock_old(decoded):
    """Encode a ticker as an integer."""
    return int(reduce(lambda x,y:x+y,map(
         lambda x:str(ord(x)),list(decoded))))


def decode_meme_stock(encoded):
    return decode_meme_stock_old(100*encoded)


def encode_meme_stock(decoded):
    encoded = encode_meme_stock_old(decoded)
    return encoded/100.0

