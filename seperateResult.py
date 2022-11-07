import pandas as pd

df = pd.read_csv('output/uk_sentimentResultCombined.csv')

df_positive = df.query('sentiment == "Positive"')
df_negative = df.query('sentiment == "Negative"')
df_neutral = df.query('sentiment == "Neutral"')
df_mixed = df.query('sentiment == "Mixed"')

# print(df_positive.info())
# print(df_positive.head())


df_positive.to_csv('output/uk_SentimentPositiveResult.csv', index=False, header=True)
df_negative.to_csv('output/uk_SentimentNegativeResult.csv', index=False, header=True)
df_neutral.to_csv('output/uk_SentimentNeutralResult.csv', index=False, header=True)
df_mixed.to_csv('output/uk_SentimentMixedResult.csv', index=False, header=True)

