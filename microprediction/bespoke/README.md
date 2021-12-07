Categorical Time Series on Microprediction
==========================================

Storing Categorical Data
------------------------
Let's begin by stating that Microprediction is not (currently) designed to store categorical data. Categorical random variables differ from continuous random variables in two important ways. Firstly, the data is not required to be measurable (in the sense of measure theory); and secondly, the values taken by the series are all arbitrary labels. A set of category labels can always be put in 1:1 correspondence with another set of labels, even numerical labels, such as the integers or the reals, but none of those labels are meaningful. In particular the differences between elements of a set of numerical labels are completely meaningless.

Microprediction is designed to store time-series of real values (as represented by IEEE 754 double precision floating point numbers). To store categorical data for streams on Microprediction requires some level of "abuse" of the currently implemented system. To help encode categorical variable labels some form of encoding must be invented. This encoding is a function that maps the set of labels to the reals (see prior note). Desirable properties of these encodings include:

1. Invertibility: if the function used to encode a label possesses an inverse that returns the label from the encoding this will be useful.
2. Statelessness: a process can always be created that maps a set of labels to an ordinal number of some kind. These ordinals would represent some kind of, potentially meaningful, indicators of the position of a label in a sequence. These kinds of mappings are only usable when there is provided a digest that is used to define the mapping between the labels and the ordinals and are, therefore, not "stateless" in the sense that the mapping function will always provide the same answer regardless of the state of the digest provided to it. Mapping functions that are stateless, meaning they are deterministic functions without a necessary digest, will be useful.
3. Readability: it would be useful for the encoded labels to be readily readable.

The Encode and Decode Functions
-------------------------------
It was decided to represent short alphanumeric labels, such as those encountered as stock market "ticker symbols," by a concatenation of their ordinal values within the well known ASCII character encoding. This represents the letter A by the number 65, the letter B by the number 66 etc. Thus a ticker symbol such as BABA can be represented by the sequences of two digit integers {65,66,65,66}. Furthermore, these sequences of two digit integers may be "run-together" to create a single integer such as 66656665, in this case. Such a number may be stored as a double precision float exactly. IEEE 754 provides at least 15 decimal place precision (sometimes 16, it depends on the number) and so at least seven character labels may be represented as a float without error.

Two python functions, encode and decode, have been provided to execute these mapping functions.

```
def encode(decoded,ceiling=1e7,scale=1e2):
    """Encode a ticker as a float."""
    f=int(reduce(lambda x,y:x+y,map(lambda x:str(ord(x)),list(decoded))))
    
    while f>ceiling:
        f/=scale
        
    return f

def decode(encoded):
    """Decode a float to a ticker."""
    f=str(encoded).replace(".","")
    return str(reduce(lambda x,y:x+y,map(lambda x:chr(int(x)),findall(r"[0-9][0-9]",f))))
```

The Impact of Microprediction's Added Noise
------------------------------------------
As Microprediction requires distributional prediction, the use of categorical data requires the submission of a view of the probability mass function of the underlying categorical data. This can be executed by a "voting" procedure in which encoded categories are submitted multiple times inline with their associated relative probability. However, the SUBMIT method in Microprediction's API requires a facility to distinguish between repeated identical predictions and it implements this via adding random noise to each submission. Due to the necessary representation of floating point numbers as binary integers under the scheme propagated by the IEEE 754 standard there can be numbers which are indistinguishable from those same numbers with added random noise. These are generally "larger integers" to which small noise is added.  For example, in Python:

```
>>> 12345e6
12345000000.0
>>> 12345e6+0.0001/225
12345000000.0
>>> assert(12345e6!=12345e6+0.0001/225)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

Thus an encoding that represents a short text string as a large integer, such as the one above, might create situations in which adding noise to the submission does not, in fact, change it. Which particular numbers are affected depends on the binary representation of the number and so is, essentially, chaotic from the users point of view. An attempt has been made to minimize this effect by dividing the encodings by a scale factor (default is 100). This may be done until the last significant digit of the encoded number is the same order of magnitude as the noise. The scaling can be reversed, to improve invertibility, by multiplying the numbers by 100 until the fractional part is removed. Alternately, it can be done by stripping out the non-digit characters from the textual representation of the number.

Meme Stock of the Hour
----------------------
The stream `meme-stock-of-the-hour.json` is an encoding of the most popular ticker symbol referenced via as "cashtag," such as $TSLA, on the subreddit `/r/wallstreetbets` in the last 24 hours. The stream updates hourly. Early data was encoded with the function `encode(ticker,ceiling=1e9)`, but this provided collisions with the added noise. From 12/05/2021 the encoding switched to `encode(ticker,ceiling=1e7)`, which is now the default setting.

Best and Worst Crypto Coin of the Hour
--------------------------------------
The streams `best-crypto-of-the-hour.json` and `worst-crypto-of-the-hour.json` are encodings of the cryptocurrency coins that have had the most extreme returns over the past sample period (which is usually one hour). The universe of coins are the 25 with the top market cap according to the page https://finance.yahoo.com/cryptocurrencies, which will be updated from time-to-time. The data is sampled via the `yfinance.Ticker.history` method, which also reads from Yahoo! Finance, and a price history file, with other added value features, is written to a public S3 bucket: https://s3.amazonaws.com/public.gillerinvestments.com/crypto-of-the-hour.json.

Pre-Submission Jittering
------------------------
If you intend to submit predictions to a discrete stream you need to submit a representation of the probability mass function. This will, by necessity, likely involve the repeating of many identical values, which is problematic for the Microprediction system. The system applies noise to permit disambiguation of submissions but sometimes this failes resulting in the _failure to submit_ condition:

```
--- SUBMIT ERRORS ---- 
[]
```

One way to prevent that is to _pre-jitter_ the submissions by a level of noise such that the least significant digit is not endangered, thereby preserving invertibility.

To learn more about these issues, feel free to contact me at mailto:graham@gillerinvestments.com
