# **How to enter a Microprediction contest**
### Required Libraries

```{r libs}
library(httr)
library(jsonlite)
```

## **1. Get data from microprediction.org**

For this introductory example, we retrieve implied z-scores for the implied copula induced by changes in IOTA and Ripple cryptocurrencies (a lot to unpack there), but you can choose any stream from <https://www.microprediction.org/browse_streams.html> Just put `.json` on the end. 

You can view this individual time series at <https://www.microprediction.org/stream_dashboard.html?stream=z2~c5_iota~c5_ripple~3555>

```{r data}
# The name of the time series. 
name <- "z2~c5_iota~c5_ripple~3555.json"      

# Download the series
lagged <- jsonlite::fromJSON(paste0("https://api.microprediction.org/lagged/",name))
x <- lagged[, 2, drop=FALSE]

hist(x, main = "Distribution of implied z-scores for IOTA price changes", col="darkmagenta")
```

## **2. Sample from the empirical density**

We need to submit 225 sorted values of our predicted distribution for each stream.

Here is an example with some recency bias, and using the `quantile()` function to evenly space our 225 samples. You will note that the values are in returned in a descending order based on date, so our most recent observations are the first ones.

This particular technique might work better with streams starting in `z1~` or `z2~` or `z3~`, but more on subsetting groups of streams later.

```{r sample}
# Create new series with most recent values first
y <- c(x[1:50], x[1:200], x) 
n <- 225

# Generate a sequence of probabilies from 1/450 : 449/450
probs <- seq(1/(2*n), 1-1/(2*n), length.out = n)

# Sample from the ECDF of the new vector
q <- quantile(y, probs = probs, names=FALSE)
head(q)

hist(q, main = "My predicted distribution", breaks = 15)
```

## **3. Create your secret identity**

There is no registration at www.microprediction.org. Instead you create your own key.  As there is no R key generator just yet, just open this python notebook in colab and run it <https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb> Grab a freshly generated key.

```{r writekey}
write_key <- "4c7b09f298bb7eb580b48ada674142cd"  # not a real key, read the above
```

We also need to set our email associated with our secret identity so we can receive our prizes!
```{r email}
email <- 'your_email@gmail.com'
res <- httr::PUT(url = paste0("https://api.microprediction.org/email/", write_key), body = list(email = email))
print(res)
```

## **4. Submit your distribution**

```{r submission, eval=FALSE}
# We have to supply values as a comma separated list 
my_values <- toString(q) 

# Then we make a PUT to the API
res <- httr::PUT(url = paste0("https://api.microprediction.org/submit/", name),
                 body = list(write_key = write_key, delay=70, values = my_values))

print(res)
```

After you submit, race over to www.microprediction.org and paste your key into the dashboard. You will also appear at <https://www.microprediction.org/leaderboard.html> under "bivariate".

# **Enter Multiple Contests**

## **1. Download Contest Names**

We can download all of the contest names and then subset on different types of streams our models may excel at.  Here we isolate just the `z1` streams.

```{r z1}
# Download all of the contest names
overall_contest_list <- names(httr::content(httr::GET(url = "https://api.microprediction.org/volumes/")))

# Split string based on the "::"
reduced_list <- strsplit(overall_contest_list, split="::")

# Split further based on "~"
further_reduced_list <- lapply(reduced_list, function(x) strsplit(x, split = "~"))

# Find just the contests that contain "z1"
z1_contest_index <- which(unlist(lapply(further_reduced_list, function(x) any(unlist(x)=="z1"))))

# Remove everything prior to "::" and save the contest names
z1 <- gsub(".*::","", overall_contest_list[z1_contest_index])

head(z1)
```

## **2. Loop through all of the names**

This is best parallelized using the `parallel` package and `foreach()` functions.

```{r foreach, eval=FALSE}
library(parallel)
library(foreach)

## For parallel processing
cores <- detectCores()
cl <- makeCluster(cores[1]-1)
registerDoParallel(cl)


results <- list()

results <- foreach(i = 1:length(z1),.packages = c("httr", "jsonlite"))%dopar%{
  write_key_cc <- "4c7b09f298bb7eb580b48ada674142cd"  # still not a real key
  
  name <- z1[i]      
  
  lagged <- jsonlite::fromJSON(paste0("https://api.microprediction.org/lagged/", name))
  
  x <- lagged[,2, drop=FALSE]
  
  # Create new series with most recent values first
  y <- c(x[1:50], x[1:200], x)
  
  # Generate a sequence of probabilies from 1/450 : 449/450
  probs <- seq(1/450, 1-1/450, length.out = 225)

  # Sample from the ECDF of the new vector
  q <- quantile(y, probs = probs, names = FALSE)
  
  my_values <-  toString(q)
  
  # You can add additional delays or change the value
  res <- httr::PUT(url = paste0("https://api.microprediction.org/submit/",name),
                   body = list(write_key = write_key, delay = 70, values = my_values))
      
  return(res)
}

parallel::stopCluster(cl)
registerDoSEQ()
```

## **3.  Sponsored Contests**

There are sponsored contests which offer daily and monthly prizes, see <https://www.microprediction.com/competitions> for more details.  This example will generate a list of streams sponsored by the MUID Offcast Goose.

```{r contests}
# Grab all sponsored contests
sponsored_contests <- httr::content(httr::GET("https://api.microprediction.org/sponsors/"))

# Create data.frame
sponsored_contests_df <- cbind.data.frame("contest" = names(sponsored_contests), "sponsor" = unlist(sponsored_contests))
rownames(sponsored_contests_df) <- NULL

head(sponsored_contests_df)

# Select individual sponsor
offcast_goose_sponsored <- sponsored_contests_df[sponsored_contests_df$sponsor == "Offcast Goose",]

# Verify
head(offcast_goose_sponsored)
```


## **4. Constant Submissions**

Here are 2 methods to constantly submit based on desired frequency:

-   Schedule the script to run via the `taskscheduleR` package on CRAN

-   Enclose the entire script in an infinite `repeat{ … }` loop with a `Sys.sleep(time = …)` call for the desired interval in submissions.


# **Publish A Stream**

Do you want a swarm of fiercely competiting algorithms to predict your data? State of the art algorithms will find your stream of data and start predicting it. They even find relevant data. The quintessential use is live, public, frequently updated data. However there are many ways to use the API for private prediction if you are sneaky.  See more uses of publishing <https://www.microprediction.com/get-predictions>.

In the same manner one would submit constant predictions via the `taskscheduleR` or `repeat{...}` loop, your stream values can be submitted analogously.

Once you have a `write_key` of difficulty 12 or higher and you have identified the data you wish to receive predictions on, you can publish the latest value `my_stream_value` using a specific name for your stream `my_stream_name`.

```{r streams}
my_stream_name <- "blah.json"

repeat{
  my_stream_value <- {Some code or retrieval generating a value to publish}

  httr::PUT(url = paste0("https://api.microprediction.org/live/", my_stream_name),
                   body = list(write_key = write_key, budget = 1, value = my_stream_value))
                   
  sys.sleep(time = …)
}
```

## **Retrieving Community Predictions**
Once you have unleashed the swarm upon your data, you can grab the predictions along with the ID associated with each submission.  Specify which `delay` you are interested in, and the raw data is returned.

We then read the raw output with `httr::content(...)` and finally format it as a matrix with the row names as the ID.

```{r grab}
my_stream_predictions_raw <- httr::GET(url = paste0("https://api.microprediction.org/live/", my_stream_name),
                                       query = list(delay = 70, write_key = write_key))
                                   
my_stream_predictions_unformatted <- httr::content(my_stream_predictions_raw)

my_stream_predictions_formatted <- t(t(my_stream_predictions_unformatted))
```
