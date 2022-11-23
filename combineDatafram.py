import pandas as pd


# read first half CSV file
df1 = pd.read_csv('spain_sentimentCombinedResult_1.csv')

# read second half CSV file
df2 = pd.read_csv('spain_sentimentCombinedResult_2.csv')

frames= [df1,df2]

result = pd.concat(frames)

# export into one CSV file
result.to_csv('spain_sentimentCombinedResult.csv')
