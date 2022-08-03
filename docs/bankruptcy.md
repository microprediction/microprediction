## Bankruptcy

The more difficult your [write key](https://microprediction.github.io/microprediction/writekeys.html), the more leeway you get to make consistenty poor predictions. 

Every participating `write_key` has an associated balance. When you create a stream you automatically participate in the prediction of the stream. A benchmark empirical sampling algorithm with some recency adjustment is used for this
purpose. If nobody can do a better job that this, your `write_key` balance will neither rise nor fall, on average.  

However once smart people and algorithms enter the fray, you can expect this default model to be beaten and the balance on your `write_key` to trend downwards. 
On an ongoing basis you also need the `write_key` balance not to fall below a threshold bankruptcy level. The minimum balance for a key of difficulty 9 is also found at https://api.microprediction.org/config.json and
 the formula:
 

<img src="https://render.githubusercontent.com/render/math?math=%5CLarge%0A-1*(abs(self.min%5C_balance)*16%5E%7B(write%5C_key%5C_difficulty-9)%7D">


supercedes whatever is written here. However, at time of writing the bankruptcy levels are:

|  write_key difficulty   |  bankruptcy         |  write_key difficulty   |  bankruptcy         |
|-------------------------|---------------------|-------------------------|---------------------|
|  8                      |  -0.01              |     11                  |   -256              |
|  9                      |  -1.0               |     12                  |   -4,096            |
| 10                      |  -16.0              |     13                  |   -65,536           |
       
You can see why your crawler may live a longer life if the key is more difficult. 

Balance may be transferred from one `write_key` to another if the recipient `write_key` has a negative balance. You can use the transfer function to keep
a `write_key` alive that you need for sponsoring a stream. You can also ask others to mine (muids)[https://github.com/microprediction/muid] for you and contribute in this fashion, say if you have an important civic nowcast and expect that others
 might help maintain it. You cannot use a transfer to 
raise the balance associated with a `write_key` above zero - that is only possible by means of accurate prediction. 


