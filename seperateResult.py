import pandas as pd

df = pd.read_csv('output/spain_sentimentResultCombined.csv')

df_positive = df.query('sentiment == "Positive"')
df_negative = df.query('sentiment == "Negative"')
df_neutral = df.query('sentiment == "Neutral"')
df_mixed = df.query('sentiment == "Mixed"')

# print(df_positive.info())
# print(df_positive.head())


df_positive.to_csv('output/spain_SentimentPositiveResult.csv', index=False, header=True)
df_negative.to_csv('output/spain_SentimentNegativeResult.csv', index=False, header=True)
df_neutral.to_csv('output/spain_SentimentNeutralResult.csv', index=False, header=True)
df_mixed.to_csv('output/spain_SentimentMixedResult.csv', index=False, header=True)

