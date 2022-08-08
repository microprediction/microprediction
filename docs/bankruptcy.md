## Bankruptcy

Bankruptcy is a basic maechanism to discourage noise predictions and spurious streams. 

### Predicting


Every participating `write_key` has an associated balance that should not fall below a threshold bankruptcy level. 

The more difficult your [write key](https://microprediction.github.io/microprediction/writekeys.html), the more leeway you get to make consistenty poor predictions. Your initial balance is zero. It will go up on down depending on how well you predict. 

|  write_key difficulty   |  bankruptcy         |  write_key difficulty   |  bankruptcy         |
|-------------------------|---------------------|-------------------------|---------------------|
|  8                      |  -0.01              |     11                  |   -256              |
|  9                      |  -1.0               |     12                  |   -4,096            |
| 10                      |  -16.0              |     13                  |   -65,536           |
       

As a technicality, this table might go out of data and the formula

<img src="https://render.githubusercontent.com/render/math?math=%5CLarge%0A-1*(abs(self.min%5C_balance)*16%5E%7B(write%5C_key%5C_difficulty-9)%7D">

supercedes it, where there is a parameter: the minimum balance for a key of difficulty 9, which can be found at https://api.microprediction.org/config.json and is subject to chage. 

### Creating streams

You can also go bankrupt creating streams, for the simple reason that this requires predition too. 

Yes, when you create a stream you automatically participate in the prediction of the stream. A benchmark empirical sampling algorithm with some recency adjustment is used for this purpose. If nobody can do a better job that this, your `write_key` balance will neither rise nor fall, on average.  

However once smart people and algorithms enter the fray, you can expect this default model to be beaten and the balance on your `write_key` to trend downwards. 

### Transfer API

Balance may be transferred from one `write_key` to another if the recipient `write_key` has a negative balance. You can use the transfer method to keep
a `write_key` alive that you need for sponsoring a stream. You can also ask others to mine (muids)[https://github.com/microprediction/muid] for you and contribute in this fashion, say if you have an important civic nowcast and expect that others
 might help maintain it. You cannot use a transfer to 
raise the balance associated with a `write_key` above zero - that is only possible by means of accurate prediction. 

### Balance bolstering methods
I suggest you look at the [writer](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) for convenient methods that can help you avoid bankruptcy. For example:

    mw = MicroWriter(write_key='YOUR KEY HERE')
    mw.put_balance(source_write_key='SOME OTHER WRITE KEY', amount=100.)

