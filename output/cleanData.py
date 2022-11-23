import pandas as pd
import numpy as np
import re
import emoji
import nltk
from glob import glob
from os import mkdir, path

nltk.download('words')
words = set(nltk.corpus.words.words())

file_names = glob(path.join('spain','*.json')) # edit folder name to folder that you want to covert all JSON file to CSV
dfs = [pd.read_json(fn, lines = True) for fn in file_names]
tweet_df = pd.concat(dfs)


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


# df = pd.read_csv('output/tweets_eu&uk_dataset.csv') #read file 

tweet_df = tweet_df[['user_id','username', 'date', 'tweet']]

tweet_df['tweet'] =tweet_df['tweet'].map(lambda x: cleaner(x))

tweet_df['tweet'] = tweet_df['tweet'].astype("string")

tweet_df.info()

nan = float("NaN")
tweet_df.replace("",nan, inplace=True)
tweet_df.dropna(subset=['tweet'],inplace=True)

tweet_df.to_csv('tweets_spain_cleaned_dataset.csv') # edit output filename

