# microprediction

A minimalist Python client for entering microprediction contests

    pip install microprediction 

Not quite ready yet, but in advance you can do step 1. below. 

### (1) Obtaining your memorable identifier

In one cut and paste:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/muid/master/examples/mine_from_venv.sh)"

Or using the library...
    
    $pip install muid
    $python3
    >>> import muid
    >>> muid.mine(skip_intro=True)
    
Be patient! Video explanation at https://vimeo.com/397352413 

### (2) Submitting predictions 

Soon you will be able to do this:

    mc = MicroClient(write_key=<YOUR PRIVATE IDENTITY HERE>) 
    scenarios = [ i*0.001 for i in range(1000) ] 
    mc.submit(name='cop.json',values=scenarios)
    

### (3) Historical data 
    
Options are: 
 
    lagged_values = mc.get_lagged_values(cop.json) 
    time_valu_pairs = mc.get_lagged(cop.json)

### (4) Prefixed get

Supplied getters have prefixed equivalents

    lagged_values = mc.get('lagged_values::cop.json')

### (5) Direct get 

Alternatively

    import requests
    lagged_values = requests.get('https://www.microprediction.com/live/lagged_values::cop.json').json()
 

    
    
 
