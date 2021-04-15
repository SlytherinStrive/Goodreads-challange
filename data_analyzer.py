import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/prepocessed_14th.csv")
# 1. Scatter plot between Number of ratings and Number of Pages
def pages_vs_ratings_scat(df):
    plt.figure(figsize=(12,5))
    plt.scatter(x='num_pages', y='num_ratings', data = df)
    plt.title('Pages vs ratings ', fontsize='20')
    plt.xlabel('Number of pages')
    plt.ylabel('Number of ratings (in mln.)')
    return plt.show()

# 2. Correlation between Number of Reviews and Number of Pages
corr_pages_review = df.corr().loc['num_pages','num_ratings']
print (f"Correlation between number of pages and rating is {round(corr_pages_review,5)}")

# 3. 3. Visualise the avg_rating distribution.
def avg_rating_dist(df):
    plt.figure(figsize=(12,5))
    sns.displot(df, x="avg_rating", kde=True, fill=True)
    plt.title('Average rating distribution', fontsize='20')
    plt.xlabel('Average rating Distribution')
    plt.show()

# 4. Visualise the minmax_norm_rating distribution.
def min_max_norm(df):
    sns.displot(df, x="minmax_norm_ratings", kde=True, fill=True)
    plt.title('MinMax Normalization distribution', fontsize='13')
    plt.xlabel('MinMax Distribution')
    plt.show()
min_max_norm(df)

# 5. Visualise the `mean_norm_rating` distribution.
def mean_norm_rating_dist(df):
    plt.figure(figsize=(12,5))
    sns.displot(df, x="normalise_mean", kde=True, fill=True)
    plt.title('Mean normalized rating distribution', fontsize='20')
    plt.xlabel('Mean normalized rating distribution')
    plt.show()

# 6. Create one graph that represents in the same figure both `minmax_norm_rating` and `mean_norm_rating`distributions.
def distributions(df):
    sns.histplot(data=df, x="normalise_mean", color="navy", label="Mean", kde=True)
    sns.histplot(data=df, x="minmax_norm_ratings", color="red", label="Min/Max", kde=True)
    plt.xlabel('Rating')
    plt.title('Min/Max and Mean Distributions', fontsize='13')
    plt.legend(loc=1)
    plt.show()
distributions(df)
#8. Visualize the `awards` distribution in a **boxplot** and **aggregated bars**. Decide which of these representations gives us more information and in which cases they should be used.
# a. boxplot
def box_awards(df):
    df[['award_count']].plot.box(vert=False, color='blue')
    plt.title('Number of Awards', fontsize='13')
    plt.show

# b.aggregate bars of total awards by books
most_awards = df.sort_values(by='award_count', ascending=False)
most_awards=  most_awards[['title','award_count']]
most_awards = most_awards.head(20)

def agg_awards(df):
    plt.figure(figsize=(10,5))
    sns.barplot(y='title', x='award_count', data =most_awards, palette="Paired")
    plt.title('15 Most Awarded Books', fontsize='13')
    plt.xlabel('Number of Awards')
    plt.ylabel('Book Title')
    plt.show()
agg_awards(df)


# 10. Make a scatterplot to represent  minmax_norm_ratings in function of the number of awards won by the book
#- Is there another representation that displays this in a more clear manner?
#- Optional: Can you plot a best fit linear regression line to represent the relationship?
def cor_award_minmax (df):
    sns.regplot(x = "award_count", y = "minmax_norm_ratings", line_kws={"color": "red"}, data = df)
    plt.xlim(0,20)
    plt.title('Correlation Between Awards Number and Min/Max Normalised Ratings', fontsize='12')
    plt.xlabel('Number of Awards')
    plt.ylabel('Min/Max Normalization')
    plt.show()
cor_award_minmax (df)

# Graph most reviewed books
def most_reviewed_books(df):
    mostly_reviewed = df.sort_values(by='num_reviews', ascending=False) # Sorting by number of reviews
    mostly_reviewed = mostly_reviewed[['title','num_reviews']] # Selecting just the columns we want
    mostly_reviewed = mostly_reviewed.head(15) # Choosing only the top 10 books
    plt.figure(figsize=(12,5))
    sns.barplot(y='title', x='num_reviews', data = mostly_reviewed, palette="tab10")
    plt.title('15 Most Reviewed Books', fontsize='20')
    plt.xlabel('Number of Reviews (in mln.)')
    plt.ylabel('Book Title')
    return plt.show()


input_dict = {
            "1":pages_vs_ratings_scat(df),
            #"2": ,
            "3": avg_rating_dist(df),
            "4": min_max_norm(df),
            "5": mean_norm_rating_dist(df),
            "6": distributions(df),
            #"7": ,
             "8":box_awards(df),
            #"9": ,
            "10":cor_award_minmax (df),
            "11": most_reviewd_books(df),

            }

finished = False
viewing = None
