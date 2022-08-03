A WRITE_KEY is a private unique identifier whose hash is partly memorable. Options for obtaining one:

### Python colab notebook

Open [notebook_examples/New_Key](https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb) and run it for hours. 

### Python 

    from microprediction import new_key
    print(new_key(difficulty=12))
    
