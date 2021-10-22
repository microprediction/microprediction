# For those looking at the meme of the day stocks

from re import findall
from functools import reduce

def decode(encoded):
    """Decode an integer to a ticker."""
    return str(reduce(lambda x,y:x+y,map(lambda x:chr(int(x)),findall(r"[0-9][0-9]",str(int(encoded))))))

def encode(decoded):
    """Encode a ticker as an integer."""
    return int(reduce(lambda x,y:x+y,map(lambda x:str(ord(x)),list(decoded))))
