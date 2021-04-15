import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from math import pi

df = pd.read_csv("data/9745_greatest_books_ever.csv")
# 1. Scatter plot between Number of ratings and Number of Pages
def pages_vs_ratings_scat(df):
    plt.figure(figsize=(12,5))
    plt.scatter(x='num_pages', y='num_ratings', data = df)
    plt.title('Pages vs ratings ', fontsize='20')
    plt.xlabel('Number of pages')
    plt.ylabel('Number of ratings (in mln.)')
    return plt.show()
#pages_vs_ratings_scat(df)

# 2. Correlation between Number of Reviews and Number of Pages
def corr_pages_review(df):
    corr_pages_review = df.corr().loc['num_pages','num_ratings']
    print (f"Correlation between number of pages and rating is {round(corr_pages_review,5)}")
#corr_pages_review(df)

# 3. Visualise the avg_rating distribution.
def avg_rating_dist(df):
    plt.figure(figsize=(12,5))
    sns.displot(df, x="avg_rating", kde=True, fill=True)
    plt.title('Average rating distribution', fontsize='20')
    plt.xlabel('Average rating Distribution')
    plt.show()
#avg_rating_dist(df)

# 4. Visualise the minmax_norm_rating distribution.
def min_max_norm(df):
    sns.displot(df, x="minmax_norm_ratings", kde=True, fill=True)
    plt.title('MinMax Normalization distribution', fontsize='13')
    plt.xlabel('MinMax Distribution')
    plt.show()
#min_max_norm(df)

# 5. Visualise the `mean_norm_rating` distribution.
def mean_norm_rating_dist(df):
    plt.figure(figsize=(12,5))
    sns.displot(df, x="normalise_mean", kde=True, fill=True)
    plt.title('Mean normalized rating distribution', fontsize='20')
    plt.xlabel('Mean normalized rating distribution')
    plt.show()
#mean_norm_rating_dist(df)

# 6. Create one graph that represents in the same figure both `minmax_norm_rating` and `mean_norm_rating`distributions.
def distributions(df):
    sns.histplot(data=df, x="normalise_mean", color="navy", label="Mean", kde=True)
    sns.histplot(data=df, x="minmax_norm_ratings", color="red", label="Min/Max", kde=True)
    plt.xlabel('Rating')
    plt.title('Min/Max and Mean Distributions', fontsize='13')
    plt.legend(loc=1)
    plt.show()
#distributions(df)

#8. Visualize the `awards` distribution in a **boxplot** and **aggregated bars**. Decide which of these representations gives us more information and in which cases they should be used.
# a. boxplot
def box_awards(df):
    df[['award_count']].plot.box(vert=False, color='blue')
    plt.title('Number of Awards', fontsize='13')
    plt.show()
#box_awards(df)

# b.aggregate bars of total awards by books
def agg_awards(df):
    most_awards = df.sort_values(by='award_count', ascending=False)
    most_awards=  most_awards[['title','award_count']]
    most_awards = most_awards.head(20)
    plt.figure(figsize=(10,5))
    sns.barplot(y='title', x='award_count', data = most_awards, palette="Paired")
    plt.title('15 Most Awarded Books', fontsize='13')
    plt.xlabel('Number of Awards')
    plt.ylabel('Book Title')
    plt.show()
#agg_awards(df)


# 10. Make a scatterplot to represent  minmax_norm_ratings in function of the number of awards won by the book
#- Is there another representation that displays this in a more clear manner?
#- Optional: Can you plot a best fit linear regression line to represent the relationship?
def cor_award_minmax (df):
    g1=sns.regplot(x = "award_count", y = "minmax_norm_ratings", line_kws={"color": "red"}, data = df, scatter_kws={'edgecolor':'white'})
    g1.figure.set_size_inches(15,10)
    plt.xlim(0,20)
    plt.ylim(6.5,10)
    plt.title('Correlation Between Awards Number and Min/Max Normalised Ratings', fontsize='20')
    plt.xlabel('Number of Awards')
    plt.ylabel('Min/Max Normalization')
    plt.show()
#cor_award_minmax (df)


#Correlation between page numbers and rankings (normalise_mean)
def corr_page_rank(df):
    g=sns.regplot(x = "num_pages", y = "normalise_mean",line_kws={"color": "red"}, data = df, scatter_kws={'edgecolor':'white'})
    g.figure.set_size_inches(15,10)
    plt.xlim(-0,1000)
    plt.ylim(3.5,7)
    plt.title('Correlation Between Page Numbers and Ranking', fontsize='20')
    plt.xlabel('Page numbers')
    plt.ylabel('Rank')
    plt.show()
    corr_pages_review = df.corr().loc["num_pages","normalise_mean"]
    print (f"Correlation between number of pages and rating is {round(corr_pages_review,4)}")
#corr_page_rank(df)


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
#most_reviewed_books(df)



########## Custom min_max_normalise to 100
def min_max_normalise(ratings):
    normalised = ((ratings - min(ratings)) / (max(ratings) - min(ratings)))
    transform = ((normalised + 1) * 49.5) + 1
    return transform
# Proves authors are better off using initals
def page_numbers_by_score_for_genres(adf):
    plt.figure(figsize=(12,5))
    uses_initials = adf[adf['author'].str.contains(".", regex=False)]
    no_initials = adf[~adf['author'].str.contains(".", regex=False)]
    uses_initials['awards_mean'] = min_max_normalise(uses_initials['award_count']).mean()
    uses_initials['ratings_mean'] = min_max_normalise(uses_initials['avg_rating']).mean()
    uses_initials['good_read_score_mean'] = min_max_normalise(uses_initials['good_read_score']).mean()
    uses_initials['good_read_votes_mean'] = min_max_normalise(uses_initials['good_read_votes']).mean()
    uses_initials['reviews_mean'] = min_max_normalise(uses_initials['num_reviews']).mean()

    no_initials['awards_mean'] = min_max_normalise(no_initials['award_count']).mean()
    no_initials['ratings_mean'] = min_max_normalise(no_initials['avg_rating']).mean()
    no_initials['good_read_score_mean'] = min_max_normalise(no_initials['good_read_score']).mean()
    no_initials['good_read_votes_mean'] = min_max_normalise(no_initials['good_read_votes']).mean()
    no_initials['reviews_mean'] = min_max_normalise(no_initials['num_reviews']).mean()
    ni = list(no_initials[['awards_mean','ratings_mean','good_read_score_mean','good_read_votes_mean', 'reviews_mean']].values)[0]
    ui= list(uses_initials[['awards_mean','ratings_mean','good_read_score_mean','good_read_votes_mean', 'reviews_mean']].values)[0]
    print(ni)
    print(ui)
    ################## THE GRAPH


    # ------- PART 1: Create background
    df = pd.DataFrame({
            'group': ['UI','NI'],
            'Good read rating': [ui[1], ni[1]],
            'Good read score': [ui[2], ni[2]],
            'Good read votes': [ui[3], ni[3]],
            'Good read reviews': [ui[4], ni[4]],
            'Award Counts': [ui[0], ni[0]],

            })
    # number of variable
    categories=list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(2)
    plt.yticks([20,40,60,80,100], color="grey", size=7)
    plt.ylim(0,100)
    plt.xticks(fontsize="x-large")
    plt.title("Author Full Names Vs Use of Initials\n", fontsize="xx-large")
    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't make a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Authors who use initials")
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values=df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Authors who use full name")
    ax.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize="x-large")

    # Show the graph
    return plt.show()
#page_numbers_by_score_for_genres(df)
