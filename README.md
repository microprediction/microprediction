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
    
 To retrieve past values:
 
    lagged = c.get_lagged(cop.json) 
    
  To retrieve an approximate cdf:
  
    
 
