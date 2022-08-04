
## Summary

The [client](https://github.com/microprediction/microprediction) assists 
use of the [microprediction api](http://api.microprediction.org/) for which 
a browser is provided at [microprediction.org](https://www.microprediction.org/).
 

|   | Task                                      | Method or function                | Full code example                                                                                                                                   | Video tutorial                                                                    |
|---|-------------------------------------------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| A | Create a write_key                        | new_key                           | [enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/enter_die_contest_one_off.py) | [python-1: Your first submission](https://www.microprediction.com/python-1)       |
| B | Publish one scalar value at a time, usually representing a live measurement.   | MicroWriter.set()                 | [creating_a_stream.py](https://github.com/microprediction/microtutorial/blob/master/examples/creating_a_stream.py)                                  | [python-4: Creating a stream](https://www.microprediction.com/python-4)           |
| C | Send 225 guesses of the next value of a stream, after a fixed quarantine period. | MicroWriter.submit()              | [enter_die_contest_one_off.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/enter_die_contest_one_off.py) | [python-2: Creating your first crawler](https://www.microprediction.com/python-2) |
| D | Retrieve community predictions (PDF) 1min, 5min, 15min or 1hr ahead.            | MicroWriter.get_own_predictions() | [defassa_dog.py](https://github.com/microprediction/microprediction/blob/master/submission_examples_golf/defassa_dog.py)                            |  [colab example](https://github.com/microprediction/microprediction/blob/master/notebook_examples/get_and_show_submitted_predictions.ipynb)                                                                                 |                  |                                                                                   |   |

Someone wanting something predicted performs A, B and D. Someone providing predictions performs A and C (mindful of the reward mechanism explained in [Collective Distributional Prediction](https://www.microprediction.com/blog/intro)).   

An extremely fast way to get familiar with two of these four key pieces of functionality is
provided in a [notebook](https://github.com/microprediction/microprediction/blob/master/submission_examples_die/first_submission.ipynb) that
you can open in colab and run on Google's dime. This will create an identity for you and enter
your algorithm in an ongoing contest to predict the next roll of a die. 


-+-

Documentation [map](https://microprediction.github.io/microprediction/map.html)
