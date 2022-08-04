## Write keys

A private unique identifier whose hash is partly memorable, as explained at [muid.org](https://www.muid.org) where there is a [video](https://vimeo.com/397352413).

Difficult keys take longer to create. You need a difficulty 12 key to create streams. You are also well served by a difficult key when making predictions, due to the 
[bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html) rules.

Here's how to create one for yourself. 

### Python

Open [notebook_examples/New_Key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) and be patient. Or:

    from microprediction import new_key
    print(new_key(difficulty=12))
    
and be patient either way. 

### Stuck
... or just bored waiting for a 13-strength key? Ping us in the [slack](https://microprediction.github.io/microprediction/slack.html)


