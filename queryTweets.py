
import snscrape.modules.twitter as sntwitter
import pandas as pd

import re
import emoji
import nltk
import config
import tweepy

nltk.download('words')
words = set(nltk.corpus.words.words())

client = tweepy.Client(bearer_token = config.BEARER_TOKEN)

query = 'flooding flood -is:retweet place_country:AC' # search keyword

start_time = '2021-10-24T00:00:00Z'
end_time = '2022-10-24T00:00:00Z'

# request twitter api
response = tweepy.Paginator(client.search_recent_tweets, query=query,
        max_results=100,
        tweet_fields=['public_metrics','context_annotations','created_at', 'lang']
        ).flatten(limit=100) # number of tweet you want


tweets = []
# loop to add each row to tweets list
for tweet in response:
    tweets.append([tweet.id,tweet.created_at,tweet.lang, tweet.text, tweet.public_metrics['retweet_count'], tweet.public_metrics['like_count']]) 

# convert to DataFrame
df = pd.DataFrame(tweets, columns=['tweet_id','created_at', 'lang', 'tweet', 'retweet_count', 'like_count'])
df['created_at'] = df['created_at'].dt.tz_localize(None)



# cleaner function for remove @ sign, http linke, Emoji and # sign
def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.distinct_emoji_list(c)) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet) 
         if w.lower() in words or not w.isalpha())
    return tweet
df['tweet'] =df['tweet'].map(lambda x: cleaner(x))

print(df.head())
# df.to_csv('tweetsCleaned.csv')

