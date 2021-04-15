import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
################################################################################
#clean genres and seperate into columns
################################################################################
def genre_column_maker(dataset):
    df = pd.read_csv(dataset)

    ## Splits all genres into different columns
    x =df.genres.str.split(',', expand=True)

    y=len(df.columns)

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

    return df.to_csv("data/15th_1k_genre.csv")


dataset = pd.read_csv('data/1k_15th_preprocessed.csv')


def page_numbers_by_score_for_genres(df):

    plt.figure(figsize=(12,5))
    uses_initials = df[df['author'].str.contains(".", regex=False)]
    no_initials = df[~df['author'].str.contains(".", regex=False)]
    
    no_initials.info()

    uses_initials.info()




page_numbers_by_score_for_genres(dataset)
