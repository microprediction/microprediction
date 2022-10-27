## Bankruptcy

Bankruptcy is a rudimentary mechanism to discourage noise predictions and spurious streams. 

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

supercedes it. There is a parameter here: he minimum balance for a key of difficulty 9. The system reads this from [https://api.microprediction.org/config.json](https://api.microprediction.org/config.json )and is subject to change. 

### Creating streams

You can also go bankrupt creating streams, for the simple reason that this requires prediction too. 

Yes, when you create a stream you *automatically participate in the prediction of the stream*. A benchmark empirical sampling algorithm with some recency adjustment is used for this purpose. You can override this by making predictions for your own stream. 

Once smart people and algorithms enter the fray, you can expect the default model to be beaten and the balance on your `write_key` to trend downwards. 

### Avoiding bankruptcy

See [transfers](https://microprediction.github.io/microprediction/transfers.html). 

[Edit](https://github.com/microprediction/microprediction/blob/master/docs/bankrupcty.md) this page. 

