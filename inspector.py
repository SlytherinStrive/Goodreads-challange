import pandas as pd

df = pd.read_csv('scraped_1000.csv')

print(len(df))

dfnonan = df.dropna()


print(df.isna().sum())
