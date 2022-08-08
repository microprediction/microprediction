## Transfers

To avoid [bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html), 
it is possible to transfer balance from one `write_key` to another. 


### Transfer API

Balance may be transferred from one `write_key` to another if the recipient `write_key` has a negative balance. You can use the transfer method to keep
a `write_key` alive that you need for sponsoring a stream. 

You cannot use a transfer to 
raise the balance associated with a `write_key` above zero - that is only possible by means of accurate prediction. 

### Balance bolstering methods
I suggest you look at the [writer](https://github.com/microprediction/microprediction/blob/master/microprediction/writer.py) for convenient methods that can help you avoid bankruptcy. For example:

    mw = MicroWriter(write_key='YOUR KEY HERE')
    mw.put_balance(source_write_key='SOME OTHER WRITE KEY', amount=100.)

### Or just ask

You can also just message me in the [slack](https://microprediction.github.io/microprediction/slack.html) if you have a good stream you need to last a long time, or a prediction experiment where bankruptcy is proving annoying. 


-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)

