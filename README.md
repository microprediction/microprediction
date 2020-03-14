# microprediction

A minimalist Python client for entering microprediction contests

    pip install microprediction 

# Reading 

It is possible to retrieve most quantities with direct web calls.

    import requests
    lagged_values = mr.get('lagged_values::cop.json')
    lagged_values = requests.get('https://www.microprediction.com/live/lagged_values::cop.json').json()

The reader adds a little convenience. 

    from microprediction import MicroReader
    mr = MicroReader()
 
    summary       = mr.get_summary('cop.json')
    current_value = mr.get('cop.json')
    lagged_values = mr.get_lagged_values('cop.json') 
    lagged_times  = mr.get_lagged_times('cop.json')
    
Approximate crowd cumulative distribution function:
    
    cdf = mr.get_cdf('cop.json',delay=70)
    
Quarantined value
    
    cdf = mr.get_delayed('cop.json',delay=70)
    

# Writing

As explained at https://vimeo.com/397352413 you need to mine a MUID to obtain write privileges. You can cut and paste this bash command into terminal:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/muid/master/examples/mine_from_venv.sh)"

Or using the MUID library...
    
    $pip install muid
    $python3
    >>> import muid
    >>> muid.mine(skip_intro=True)
   
Once you have a MUID (termed a write_key in our context):   

    from microprediction import MicroWriter
    mw = MicroWriter(write_key='53e6fbba-2dcd-486c-a4ab-14759db58dde')  # Sub in your own MUID 
    
## Submitting predictions 
    
    scenarios = [ i*0.001 for i in range(mw.num_predictions) ] 
    mw.submit(name='cop.json',values=scenarios)    

## Submitting data to be predicted

You can use the writer to create a stream of live data that clever algorithms and humans can predict.

### Qualifying

You can write a new stream if:

    len(mw.animal())>mw.min_len     # You have a hard to find MUID
    
or 

    mw.balance()>mw.min_balance     # You've been good at predicting things
    
See https://www.microprediction.com/config.json for the current value of min_len and see the video explanation of your MUID spirit animal at https://vimeo.com/397352413, if it is not already obvious from the mining results.   

### Updating the current value

Set current value and receive crowd predicted prctl

    prctl = mw.put(name='mystream.json',value=3.14157) 

Retrieve other quarantined crowd percentiles

     cdf = mr.get_cdf('cop.json',delay=70,values=[0,0.5])
     
Other functionality on the way
    
## Logs

Limited logging information may be retrieved:
    
    get_errors()
    
as an alternative to the direct call:

    error_log = requests.get('https://www.microprediction.com/live/errors::53e6fbba-2dcd-486c-a4ab-14759db58dde.json').json()
 
