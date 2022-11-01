
# Twitter Sentiment and Text analysis with Azure Cognative service

This project is about sentiment and text analysis by using python and azure cognative service.
The objective of this project to find the impact of climate change of human wellbeing focus on flooding.

## Data processing: 
- Data collection from Twitter
- Data cleansing 
- Sentiment analysis (using Azure cognative service)
- Seperate result (Positiv, Negative, Neutral)
- Keyphrases extraction (using Azure cognative service)

## Data processing flowchart

![flowchart with out twitter api](./assets/flowchart.png)

### Data collection and cleansing
#### Without Twitter api token 
If you don't have Twitter API token. You can use sncrape libraly instead. But the negative point is sncrape __not allow to query tweet on specific geographic and not show the geographic information of tweet__.

You can set limit number that you want on limit variable and the keyword that you want to search on query variable
```python
query = '"climate change" (flood OR flooding) lang:en until:2022-10-25 since:2021-10-25 -filter:replies'
tweets = []
limit = 50
```

For query tweet just run 
```python
python3 queryTweetNoApi.py
```
Then you will get the CSV file name __tweetCleanedNoApi.py__. This data already cleaned (remove http links, emojis and hashtag sign) 
#### With Twitter api token 
You can get Twiiter API token from [here](https://developer.twitter.com/en)\
Twitter API token also not provide geograhic information. For get geograhic infomation you need Twiiter API Academic research Token.

```python
client = tweepy.Client(bearer_token = <YOUR_BEARER_TOKEN>)

query = 'flooding flood -is:retweet' # search keyword

# if you have Academic token you can query specific time
start_time = '2021-10-24T00:00:00Z' 
end_time = '2022-10-24T00:00:00Z'

# request twitter api
response = tweepy.Paginator(client.search_recent_tweets, query=query,
        max_results=100,
        tweet_fields=['public_metrics','context_annotations','created_at', 'lang']
        ).flatten(limit=100) # number of tweet you want
```

For query tweet just run 
```bash
python3 queryTweets.py
```
Then you will get the CSV file name __tweetCleanedApi.py__. This data already cleaned (remove http links, emojis and hashtag sign) 

### Sentiment analysis
After that using Azure cognative service for Sentiment analysis. You need to create Azure account. then create cognative service (Language Service) on Azure. You will get the endpoint URL and Keys for connect to the service.
![Azure cognative service](./assets/azure.png)

For connect to Sentiment analysis Azure 
add your __ENDPOINT__ and __KEYS__ in __sentiment.py__
```python
subscription_key = '<YOUR_SUBSCRIPTION_KEY>'
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
endpoint = "<YOUR_ENDPOIN_URL>"

sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
```
Then run __sentiment.py__
```bash
python3 sentiment.py
```
After run this script, You will get __sentimentResult.csv__.\
 This table contain 3 columns
 - Sentiment result
 - Number of positive words
 - Number of negative words
 - Number of neutral words

 Next step we will combine __sentimentResult.csv__ with __tweetCleanedNoApi.csv__\
 By running __combineResult.py__
 ```bash
python3 combineResult.py
```
The result is __sentimentResultCombined.csv__ before move to next step. We should use this file for analysis the result of sentiment.

### Keyphrases Extraction 
After we get sentiment result we have to seperate the result in 3 group (positive, negative, neutral) by running __seperateSentimentResult.py__
 
 ```bash
python3 seperateSentimentResult.py
```
The output has 3 files
- sentimentResult_Negative.csv
- sentimentResult_Positve.csv
- sentimentResult_Neutral.csv

Now we ready for Keyphrases extraction.First set up the __subscription_key__ and __ENDPOINT_URL__ same as sentiment analysis.
```python
subscription_key = '<YOUR_SUBSCRIPTION_KEY>'
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
endpoint = "<YOUR_ENDPOIN_URL>"
keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"
```
run this script for get the result of keyphrases extraction from Azure
 ```bash
python3 keyphrasesExtraction.py
```
Then we will get the CSV file that ready for analytics\
This table contain 10 columns
- __created_at__ Time that tweet was created
- __user__ Username of tweet
- __tweet__ tweet text
- __location__ locaiton of tweet
- __sentiment__ sentiment result 
- __positive__ Number of positive words
- __negative__ Number of negative words
- __neutral__ Number of neutral words
- __keyPhrases__ list of keywords
- __keyword__ explode __keyPhrases__ into one word __That mean one tweet can have many row__.
