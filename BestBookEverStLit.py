import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


st.title("How To Write The Best Book Ever")
st.title("Author: Gamar Fargab")


st.set_option('deprecation.showPyplotGlobalUse', False) #This line removed the error******************************

df = pd.read_csv("data/9745_greatest_books_ever.csv")
st.dataframe(df)



# 2. Correlation between Number of Reviews and Number of Pages
corr_pages_review = df.corr().loc['num_pages','num_ratings']
print (f"Correlation between number of pages and rating is {round(corr_pages_review,5)}")

# ****************************************
"""
The Minmax Normalised Rating Distribution.
"""
# ****************************************
# 4. Visualise the minmax_norm_rating distribution.
sns.displot(df, x="minmax_norm_ratings", kde=True, fill=True)
plt.title('MinMax Normalization distribution', fontsize='13')
plt.xlabel('MinMax Distribution')
plt.show()
st.pyplot()  # ****************************************


# ****************************************
"""
Minmax Normalised Rating and Mean Normalised Rating Distributions.
"""
# ****************************************
# 6. Create one graph that represents in the same figure both `minmax_norm_rating` and `mean_norm_rating`distributions.
sns.histplot(data=df, x="normalise_mean", color="navy", label="Mean", kde=True)
sns.histplot(data=df, x="minmax_norm_ratings", color="red", label="Min/Max", kde=True)
plt.xlabel('Rating')
plt.title('Min/Max and Mean Distributions', fontsize='13')
plt.legend(loc=1)
plt.show()
st.pyplot()  # ****************************************

# ****************************************
"""
Boxplot Awards Distribution
"""
# ****************************************

#8. Visualize the `awards` distribution in a **boxplot** and **aggregated bars**. Decide which of these representations gives us more information and in which cases they should be used.
# a. boxplot
df[['award_count']].plot.box(vert=False, color='blue')
plt.title('Number of Awards', fontsize='13')
plt.ion()  # ****************************************
plt.show()
st.pyplot()  # ****************************************

# ****************************************
"""
Aggregate Bars Of Total Awards By Books
"""
# ****************************************

# b.aggregate bars of total awards by books
most_awards = df.sort_values(by='award_count', ascending=False)
most_awards=  most_awards[['title','award_count']]
most_awards = most_awards.head(20)

plt.figure(figsize=(10,5))
sns.barplot(y='title', x='award_count', data = most_awards, palette="Paired")
plt.title('15 Most Awarded Books', fontsize='13')
plt.xlabel('Number of Awards')
plt.ylabel('Book Title')
plt.show()
st.pyplot()  # ****************************************


# 10. Make a scatterplot to represent  minmax_norm_ratings in function of the number of awards won by the book
#- Is there another representation that displays this in a more clear manner?
#- Optional: Can you plot a best fit linear regression line to represent the relationship?

# ****************************************
"""
Correlation Between The Number Of Awards and Min/Max Normalised Ratings
"""
# ****************************************

def cor_award_minmax (df):
    sns.regplot(x = "award_count", y = "minmax_norm_ratings", line_kws={"color": "red"}, data = df)
    plt.xlim(0,20)
    plt.title('Correlation Between Awards Number and Min/Max Normalised Ratings', fontsize='12')
    plt.xlabel('Number of Awards')
    plt.ylabel('Min/Max Normalization')
    plt.show()
    st.pyplot() # ****************************************

cor_award_minmax (df)



# Graph most reviewed books
def most_reviewd_books(df):
    mostly_reviewed = df.sort_values(by='num_reviews', ascending=False) # Sorting by number of reviews
    mostly_reviewed = mostly_reviewed[['title','num_reviews']] # Selecting just the columns we want
    mostly_reviewed = mostly_reviewed.head(15) # Choosing only the top 10 books
    plt.figure(figsize=(12,5))
    sns.barplot(y='title', x='num_reviews', data = mostly_reviewed, palette="tab10")
    plt.title('15 Most Reviewed Books', fontsize='20')
    plt.xlabel('Number of Reviews (in mln.)')
    plt.ylabel('Book Title')
    return plt.show()

def plotCorrelationMatrix(df, graphWidth):
    filename = df
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    return plt.show()

def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    return plt.show()



input_dict = {
            "1": most_reviewd_books(df),
            "2": plotCorrelationMatrix(df, 8),
            "3": plotPerColumnDistribution(df, 10, 5),
            }


st.write("Check out the repository: [link](https://github.com/SlytherinStrive)")
