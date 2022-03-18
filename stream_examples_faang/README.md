Raw [stream list.json](https://raw.githubusercontent.com/microprediction/microprediction/master/stream_examples_faang/stream_list.json) provides links. 

## MultiChangePoll


For a minimalist example of using MultiChangePoll see [faang_simple.py](https://github.com/microprediction/microprediction/blob/master/stream_examples_faang/faang_simple.py). In contrast [faang.py](https://github.com/microprediction/microprediction/blob/master/stream_examples_faang/faang.py) is more complicated as it uses the change_func option
to expand the set of numbers that are published. 


## Daily Prize 

The [faang.py](https://github.com/microprediction/microprediction/blob/master/stream_examples_faang/faang.py) example also provides some transparency into the creation of some streams used for the [daily prize](https://www.microprediction.com/competitions/daily). Some conventions for FAANG stocks and portfolios thereof can be found in the utilities [live/faang.py](https://github.com/microprediction/microprediction/blob/master/microprediction/live/faang.py) included in the microprediction client.  


## Daily Prize example StreamSkaters

See also [crawler_skater_examples](https://github.com/microprediction/microprediction/tree/master/crawler_skater_examples) for crawlers that use the timemachines package to attack the equity return streams. 

 - [Datable Llama](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py) moving average ensemble
 - [Secable Llama](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/secable_llama.py) moving average ensemble
 - [Cobego Bobcat](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/cobego_bobcat.py) aggressive moving avg ensemble
 - [Coecal Bobat](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/coecal_bobcat.py) ensemble of composed models 
 - [Leachy Bobcat](https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/leachy_bobcat.py) ensemble of models with high Elo ratings
