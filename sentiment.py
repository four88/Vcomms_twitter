import pandas as pd
import requests
from decouple import config

subscription_key = config('subscription_key', default='')
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
endpoint = "https://climatechangecog.cognitiveservices.azure.com/"

sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"


def comment_sentiment(comment=None, cid=None):
    """
    Take a single comment in string and analyze the sentiment

    Args:
        comment --  The text content to analyze.
        cid -- The numeric id of the comment analyzed.
    """
    language = "en"
    try:
        document = {"id": cid, "language": language, "text": comment}
        body = {"documents": [document]}
        res = requests.post(sentiment_url,  headers=headers, json=body)
        data = res.json()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def comment_summary(sentimentResult):
    """
        Take a single response data from comment_sentiment function and summarizes the result

        Args:
            sentimentResult --  The text response data to summarize.
    """

    summary = {"Id": 0, "Sentiment": "",
               "Positive": 0, "Neutral": 0, "Negative": 0}
    for document in sentimentResult['documents']:
        summary["Sentiment"] = document['sentiment'].capitalize()
        summary["Id"] = document['id']
        for each in document['sentences']:
            sentimentscore = each['sentiment']
            if sentimentscore == 'positive':
                summary["Positive"] += 1
            elif sentimentscore == 'negative':
                summary["Negative"] += 1
            else:
                summary["Neutral"] += 1
    return summary


def main(comment_df):
    """
    Take the data frame, get the sentiments and save the result to a CSV file

    Args:
        comment_df -- Data frame containing the text to analyze.
    Returns:
         A data frame consisting of the relevant columns
         'id','sentiment', 'positive','negative','neutral'.
    """
    df2 = comment_df
    # Drop any existing index and use a new one
    df2.reset_index(drop=True, inplace=True)
    print(u"Processing records in data frame....")
    for i, row in df2.iterrows():
        print(u"Processing Record... #{}".format(i+1))
        text_data = df2.loc[i, "tweet"].encode(
            "utf-8").decode("ascii", "ignore")
        sentimentResult = comment_sentiment(text_data, i+1)
        sentimentSummary = comment_summary(sentimentResult)
        # Add result to data frame
        df2.loc[i, "id"] = i+1
        df2.loc[i, "sentiment"] = sentimentSummary['Sentiment']
        df2.loc[i, "positive"] = sentimentSummary['Positive']
        df2.loc[i, "negative"] = sentimentSummary['Negative']
        df2.loc[i, "neutral"] = sentimentSummary['Neutral']
        dfx = df2[['id', 'sentiment', 'positive', 'negative', 'neutral']]
    print(u"Processing completed....")
    # Ensure that numbers are represented as integers and not float
    convert_dict = {'id': int,
                    'positive': int,
                    'negative': int,
                    'neutral': int,
                    'sentiment': str
                    }

    dfx = dfx.astype(convert_dict)
    return dfx


if __name__ == "__main__":
    # read comment data from csv
    commentData = pd.read_csv(
        "tweetsCleanedNoApi.csv")

    # Remove duplicated record but keep the first occurence of the record
    commentData.drop_duplicates(keep='first', inplace=True)
    # Reindex the data frame to prevent gaps in the indexes
    commentData.reset_index(drop=True, inplace=True)
    df = main(commentData)
    df.to_csv('sentimentResult2.csv', index=False, header=True)
