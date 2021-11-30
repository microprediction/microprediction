from re import findall
from functools import reduce

# Utilities for the Meme stock of the hour streams


def decode_meme_stock(encoded):
    """Decode an integer to a ticker."""
    return str(reduce(lambda x,y:x+y,map(
        lambda x:chr(int(x)),findall(r"[0-9][0-9]",
        str(int(encoded))))))


def encode_meme_stock(decoded):
    """Encode a ticker as an integer."""
    return int(reduce(lambda x,y:x+y,map(
         lambda x:str(ord(x)),list(decoded))))

