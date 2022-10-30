import pandas as pd

main_df = pd.read_csv('tweetsCleanedNoApi2.csv');
sentiment_df = pd.read_csv('sentimentResult.csv');

main_df['sentiment'] = sentiment_df['sentiment']
main_df['negative_count'] = sentiment_df['negative']
main_df['positive_count'] = sentiment_df['positive']
main_df['neutral_count'] = sentiment_df['neutral']

main_df.to_csv('sentimentResultCombined.csv')
