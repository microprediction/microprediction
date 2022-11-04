
# Ongoing model residual analysis
The no-brainer use of the world's only microprediction oracle. See Chapter 9 of the [book](https://mitpress.mit.edu/9780262047326/microprediction/). 

### Steps:
   
   1. Publish model residuals (see [publishing docs](https://microprediction.github.io/microprediction/publish.html))
 
(I guess if you are lazy you could send me a really long skinny CSV, though live is the quintessential use case)

### Why?

Someone, somewhere might have deployed an algorithm that finds signal in your noise. Or they might in the future. 

### What happens:

 - You'll add to the list of [streams](https://www.microprediction.org/browse_streams.html).
 - Algorithms (Python, Julia, R mostly) fight to predict your residuals (distributionally)
 - More arrive all the time. See [github/microprediction](https://github.com/microprediction) for an explanation of how new methods trickle in from the Python ecosystem. But anyone can deploy algorithms using R, Julia or whatever as well. 
 - The ongoing battles produce beautiful community cumulative distribution functions, such as the [CDF](https://www.microprediction.org/stream_dashboard.html?stream=faang_1&horizon=3555) representing the 1-hour ahead
forecasts of the logarithm of META price changes. 
 - You may glean quite a lot from the outcome of that fight, especially if the winners aren't "null hypothesis" algorithms.    


### Optional steps:

   2. (optional) Submit a distributional prediction of your own residuals (see [prediction docs (https://microprediction.github.io/microprediction/predict.html)) 

   3. Check with compliance. 

   4. Use set_repository() method to point people to a page containing information. 
   
   6. Add to the [rewards](https://www.microprediction.com/competitions/daily) for good prediction determined daily.

### Why is Intech allowing other funds to use this?

Read the [book](https://mitpress.mit.edu/9780262047326/microprediction/). 

![book_cover_with_blurb](/microprediction/assets/images/book_cover_with_blurb.png)

-+- 

Documentation [map](https://microprediction.github.io/microprediction/map.html) 

View [source](https://github.com/microprediction/microprediction/blob/master/docs/README.md)

![](https://github.com/microprediction/microprediction/blob/master/docs/assets/images/cotton_microprediction_3d_down.png)

