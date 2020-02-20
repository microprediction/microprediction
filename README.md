# microprediction

A minimalist Python client for entering microprediction contests

    pip install microprediction 
 

### Intech Supercollider Challenge

Before using this library: 

- Sign up for an algorithmia account https://algorithmia.com/signup
- Register at https://algorithmia.com/algorithms/threezaemails/Register to receive a write_key

Then submit or modify your scenarios as follows: 

    from microprediction.collider import Collider 
    c = Collider(write_key=<YOUR WRITE KEY HERE>) 
    scenarios = [ i*0.001 for i in range(1000) ] 
    c.submit(name='cop.json',values=scenarios)
    
 Of course those scenarios are unlikely to reflect a probabilistic representation of the future so here
 is an easy way to get lagged values: 
 
    c.get_lagged(cop.json) 
    
 

