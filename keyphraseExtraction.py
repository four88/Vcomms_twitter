import pandas as pd
import requests
from decouple import config

subscription_key = config('subscription_key', default='')
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
endpoint = "https://vcomcog.cognitiveservices.azure.com/"
keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"

# funciton to send req to azure cognative api
def tweet_keyphrase(tweet=None, cid=None):
    language = "en"
    try:
        document = {"id": cid, "language": language, "text": tweet}
        body = {"documents": [document]}
        res = requests.post(keyphrase_url, headers=headers, json=body)
        data = res.json()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# loop all tweet text and using tweet_keyphrases fucntion 
def main(tweet_df):
    keyphrases = []
    df2 = tweet_df
    # Drop any existing index and use a new one
    df2.reset_index(drop=True, inplace=True)
    print(u"Processing records in data frame...")
    for i, row in df2.iterrows():
        print(u"Processing Record... #{}".format(i+1))
        text_data = df2.loc[i, "tweet"].encode(
                "utf-8"
                ).decode("ascii", "ignore")
        keyphraseResult = tweet_keyphrase(text_data, i+1)

        #loop document to get only keyPhrases value
        for document in keyphraseResult['documents']:
            keyphrases.append(document['keyPhrases'])

    return keyphrases
    print(u"Processing completed....")



if __name__ == "__main__":
    tweetData = pd.read_csv("output/uk_SentimentMixedResult.csv") #chagne file to read here

    tweetData.reset_index(drop=True, inplace=True)
    keyphrasesResult = main(tweetData)
    tweetData['keyPhrases']  = keyphrasesResult
    
    # create same column as keyPhrases for explode each word
    tweetData['keyWord'] = keyphrasesResult

    # Exploded lists to rows of the subset columns; index will be duplicated for these rows 
    tweetData = tweetData.explode('keyWord')

print(tweetData.head())
tweetData.to_csv('output/keyphrases_result/uk_mixed_keyphrasesResult.csv', index=False, header=True)
