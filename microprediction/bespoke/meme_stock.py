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

# Versions that permit an upper limit to be placed on the encoded value to deal with precision/rounding issues.
def decode_meme_stock(encoded,epsilon=0.1e0,scale=1e2):
    """Decode a float to a ticker. Values with parts more than epsilon will be increased by scale until this is no longer true."""
    f=float(encoded)
    
    while abs(f-float(int(f)))>epsilon:
        f*=scale
    
    return str(reduce(lambda x,y:x+y,map(lambda x:chr(int(x)),findall(r"[0-9][0-9]",str(int(f))))))

def encode_meme_stock(decoded,ceiling=1e7,scale=1e2):
    """Encode a ticker as a float. Values in excess of ceiling will be reduced by scale until they are not in excess."""
    f=int(reduce(lambda x,y:x+y,map(lambda x:str(ord(x)),list(decoded))))
    
    while f>ceiling:
        f/=scale
        
    return f
