import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import emoji
import nltk

nltk.download('words')
words = set(nltk.corpus.words.words())

# location geocode
uk_geo = "geocode:54.153709,-4.529766,527km"
th_geo = "geocode:9.776238,7.742880,800km"
eu_geo = "geocode:54.321720,0.853746,2050km"

query = '"climate change" (flood OR flooding) lang:en -filter:replies ' + eu_geo 
print(query)
tweets = []
limit = 50000

print(u"Processing records in data frame...")
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])

df = pd.DataFrame(tweets, columns=['created_at', 'user', 'tweet'])
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

df.to_csv('output/tweetsCleanedNoApi_eu.csv')
print(u"Processing completed....")
