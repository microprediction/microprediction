//The program below is to send an HTTP request to the server of micropredictions to check for streams (sending request to check our stream)
import java.io.BufferedReader; import java.io.InputStreamReader; import java.net.HttpURLConnection; import java.net.URL;

public class MyPredictionModel {
    public static void main(String[] args) {
      try{
      //Defining a URL string that includes the stream name and write key. And also horizon, which is an hour for the code below.
          String url = "http://api.microprediction.org/lagged/quick_yarx_abbv.json";
          URL obj = new URL(url);
          HttpURLConnection con = (HttpURLConnection) obj.openConnection();
      //The request to get is set first to then be sent to the server
          con.setRequestMethod("GET");
      //The request for information set at the previous code is sent to the server
            int responseCode = con.getResponseCode();
            System.out.println("\nSending 'GET' request to URL : " + url);
            System.out.println("Response Code : " + responseCode);

            //The response from the server is read
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = in.readLine()) != null)
            {response.append(inputLine);}
            in.close();
      //Response from the server that is read will be printed to the console
            System.out.println(response.toString());}
      //Catches any exceptions that occur during the process and prints to the console
        catch (Exception e) {
            e.printStackTrace();}}}
