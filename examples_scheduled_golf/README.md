## Defassa Dog

The submitter is DEFASSA_DOG and it is trying to predict
 streams like [tour_17](https://www.microprediction.org/stream_dashboard.html?stream=tour_17). That stream
  shows the score obtained by all PGA Tour players on the 17th hole. To approach this, we use
  ELFEST_BOBCAT to create similar but different auxiliary streams:
  
   * [tour_17_great](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_great)
   * [tour_17_good](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_good)
   * [tour_17_okay](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_okay)
   * [tour_17_bad](https://www.microprediction.org/stream_dashboard.html?stream=tour_17_bad)
   
This breaks down the player ability into four categories. Further, the stream [tour_17_sg_total](https://www.microprediction.org/stream_dashboard.html?stream=tour_1_sg_total) reports
the mean ability of players who are likely to play the 17th hole soon. So, the only thing Defassa Dog does is
 look up the mean ability and then choose one of the auxiliary streams according to this classification. It pulls
 15 minute and one hour ahead predictions (using the ELFEST_BOBCAT key, only the stream creator can access) and then reshapes
 them in a sensible way into values to submit to [tour_17](https://www.microprediction.org/stream_dashboard.html?stream=tour_17).
 


