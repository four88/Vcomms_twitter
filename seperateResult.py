import pandas as pd
from credential import client


client = client()

df = pd.read_csv('SentimentResult.csv')

df.columns = ['Id', 'Date', 'User', 'Tweet', 'Sentiment', 'Score']

df_positive = df.query('Sentiment == "positive"')
df_negative = df.query('Sentiment == "negative"')
df_neutral = df.query('Sentiment == "neutral"')

negativeTweet = []
# df_negative.to_csv('negativeResult.csv')
for tweet in df_negative['Tweet']:
   negativeTweet.append(tweet) 

response  = client.extract_key_phrases(documents=negativeTweet)


for post in response:
    for key_phrase in post.key_phrases:
        print(key_phrase)
