# microprediction

Collective microprediction client leveraging www.microprediction.com 

    pip install microprediction 
    
# Read client

It is possible to retrieve most quantities at www.microprediction.com with direct web calls such as https://www.microprediction.com/live/cop.json. For example:


    import requests
    lagged_values = mr.get('lagged_values::cop.json')
    lagged_values = requests.get('https://www.microprediction.com/live/lagged_values::cop.json').json()

However the reader client adds a little convenience. 

    from microprediction import MicroReader
    mr = MicroReader()
 
    summary       = mr.get_summary('cop.json')
    current_value = mr.get('cop.json')
    lagged_values = mr.get_lagged_values('cop.json') 
    lagged_times  = mr.get_lagged_times('cop.json')
    delayed       = mr.get_delayed('cop.json',delay=70)
    
Your best reference is the code https://github.com/microprediction/microprediction/blob/master/microprediction/reader.py 
    
# Write client

The write client is used to submit predictions or to create a data stream. 

## Submitting predictions 

To predict a data stream at www.microprediction.com is to supply a collection of scenarios. These scenarios are quarantined for different horizons (see delays parameter at https://www.microprediction.com/config.json ). When
the data is updated by the stream owner, rewards are calculated. People and machines making accurate probabilistic forecasts will see their balances (at www.microprediction.com/balance/YOUR_WRITE_KEY)
rise. 

### Step 1: Obtaining a write_key (muid.org)

Click on http://www.muid.org/create/ to create a write_key. Hash memorable keys are explained at https://vimeo.com/397352413   
    

### Step 2: Instantiate a writer 

    from microprediction import MicroWriter
    mw = MicroWriter(write_key=)    # Sub in your own write_key 
    
### Step 3: Submitting scenarios 
    
    scenarios = [ i*0.001 for i in range(mw.num_predictions) ] 
    mw.submit(name='cop.json',values=scenarios)    

There is no difference when predicting regular streams and derived streams. For example to predict the implied z-score: 

    my_scenarios = sorted(list(np.random.randn(mw.num_predictions))
    mw.submit(name="z1~airp-06820.json", write_key="ce169feeb3565b282d50a850dc62e0db", values = my_scenarios, delay=15)

# Submitting data to be predicted

You can also use the writer to create a stream of live data that clever algorithms and humans can predict. 

    mw = MicroWriter(write_key=write_key)

However there is a higher barrier to entry...

### Step 1: Obtaining a rare write_key

To create a new stream you need:

    len(muid.animal(write_key))  >  official minimum length     # 12 at time of writing

To mine for write_keys with this property you can cut and paste this bash command into terminal:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/microprediction/muid/master/examples/mine_from_venv.sh)"

or use the MUID library (www.muid.org) ...
    
    $pip install muid
    $python3
    >>> import muid
    >>> muid.mine(skip_intro=True)
    
On an ongoing basis you also need the write_key not to go broke  

    mw.balance(write_key)  >   official minimum balance         # Not broke
    
See https://www.microprediction.com/config.json for the current values of min_len and min_balance. See
https://vimeo.com/397352413 for explanation of muid.animal(), also called the difficulty. You can always
check the difficulty of a write_key by entering a URL like http://www.muid.org/validate/fb74baf628d43892020d803614f91f29 

### Step 2: Updating the current value 

To create a new live data source or update its value:

    prctl = mw.put(name='mystream.json',value=3.14157) 

By default this returns a percentile so you know how surprising the data point is, relative to the CDF of predictions
made by others at some time in the past.   

### Step 3: Retrieve the distribution of future values

You can see what others think about the future of your data as follows:

     cdf = mw.get_cdf('cop.json',delay=mr.delays[0],values=[0,0.5])
     
where the delay parameter, in seconds, acts as a prediction horizon. This call will reveal the probability that your future value is less than 0.0, and the probability that it is 
less than 0.5. 
         
### Stream name rules 

 - Must end in .json  
 - Must contain only alphanumeric, hyphens, underscores, colons (discouraged) and at most one period.
 - Must not contain double colon. 

         
### Troubleshooting 

Limited logging information may be retrieved:
    
    mw.get_errors()
    
or

    error_log = requests.get('https://www.microprediction.com/live/errors::53e6fbba-2dcd-486c-a4ab-14759db58dde.json').json()
 
