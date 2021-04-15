import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from math import pi
################################################################################
#clean genres and seperate into columns
################################################################################
def genre_column_maker(dataset):
    df = pd.read_csv(dataset)

    ## Splits all genres into different columns
    x =df.genres.str.split(',', expand=True)

    y=len(x.columns)

    df[[f"genre_{i}" for i in range(0,y)]] = df.genres.str.split(',', expand=True)

    ### Returns a dataframe that has booleans for whether data is duplicated across columns
    is_duplicate = df[[f"genre_{i}" for i in range(0,20)]].apply(pd.Series.duplicated, axis=1).reset_index()

    ## Takes the current dataframe and where the 'is_duplicate' dataframe has True values, it replaces them with np.nan
    df[[f"genre_{i}" for i in range(0,20)]] = df[[f"genre_{i}" for i in range(0,20)]].where(~is_duplicate, np.nan).fillna('zzzyyyy')

    # A way to change nan values to another value
    for i in range(20):
        df[f"genre_{i}"] = df[f"genre_{i}"].str.strip()

    ################################################################################
    # Find the most common genres
    ################################################################################

    ## Returns 2 numpy arrays of the unique values and there counts
    unique, counts  = np.unique(df[[f"genre_{i}" for i in range(0,20)]].values, return_counts=True)

    ##zips the 2 arrays into a dictionary of "Genre": int (Count)
    d = dict(zip(unique, counts))
    # Creates a new dataframe from the dictionary with the counts as a column and the genre as the index
    genre_df = pd.DataFrame.from_dict(d, orient='index',columns=['count'])
    genre_df.drop(['zzzyyyy'], inplace=True)
    order_genre = genre_df.sort_values('count', ascending=False)
    top_50_genres = order_genre.head(50)
    genre_names = list(top_50_genres.index)
    #top_50_genres.to_csv("data/top_50_genres.csv")
    #################################################################################
    # Make columns with genre names and map true or false if book contains that genre
    #################################################################################

    for genre in genre_names:
        df[genre] = df['genres'].str.contains(genre)
        df[genre] = df[genre].map({True: 'Yes', False: 'No'})

    df.drop([f"genre_{i}" for i in range(0,20)], inplace=True, axis=1)
    df.drop(df.columns[[0,1]], axis=1, inplace=True)

    return df.to_csv("data/9745_greatest_books_ever.csv")


def min_max_normalise(ratings):
    normalised = ((ratings - min(ratings)) / (max(ratings) - min(ratings)))
    transform = ((normalised + 1) * 49.5) + 1
    return transform

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

# Set data


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
    plt.ylim(40,85)
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
    plt.show()


#page_numbers_by_score_for_genres(dataset)
