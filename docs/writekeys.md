## Write keys

Your ticket to entry is a private unique identifier whose hash is partly memorable, as explained at [muid.org](https://www.muid.org) where there is a [video](https://vimeo.com/397352413). Consider this proof
of work to be a primitive mechanism obviating registration, yet throttling some attacks. 

That's because difficult keys take longer to create. You need a difficulty
12 key to create streams (and 13 for copula streams). You are also well served by a difficult key when making predictions, due to the 
[bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html) rules.


### Option 1. Python

Open [notebook_examples/New_Key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) and be patient. 

Or:

    from microprediction import new_key
    print(new_key(difficulty=12))


### Option 2. Beg

If you are bored waiting for a 13-strength key you absolutely need? Ping us in the [slack](https://microprediction.github.io/microprediction/slack.html)

You can also politely request a balance boost, if [bankruptcy](https://microprediction.github.io/microprediction/bankruptcy.html) is proving annoying or 
is likely to be so. 

-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html)


