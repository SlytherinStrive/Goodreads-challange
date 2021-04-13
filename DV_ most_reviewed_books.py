import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("scraped_2000.csv")

#The most reviewed books
mostly_reviewed = df.sort_values(by='num_reviews', ascending=False) # Sorting by number of reviews
mostly_reviewed = mostly_reviewed[['title','num_reviews']] # Selecting just the columns we want
mostly_reviewed = mostly_reviewed.head(15) # Choosing only the top 10 books

# The 15 mostly reviewed books
plt.figure(figsize=(12,5))
sns.barplot(y='title', x='num_reviews', data = mostly_reviewed, palette="tab10")
plt.title('15 Most Reviewed Books', fontsize='20')
plt.xlabel('Number of Reviews (in mln.)')
plt.ylabel('Book Title')

plt.show()
