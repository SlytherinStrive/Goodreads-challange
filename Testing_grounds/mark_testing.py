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

dataset = "data/9745_greatest_books_ever.csv"
def award_column_maker(dataset):
    a = pd.read_csv(dataset)
    ## Splits all genres into different columns
    xx = len(a.awards.str.split(',', expand=True).columns)
    a[[f"a_{i}" for i in range(xx)]] = a.awards.str.split(',', expand=True)

    is_duplicate = a[[f"a_{i}" for i in range(0,20)]].apply(pd.Series.duplicated, axis=1).reset_index()

    ## Takes the current dataframe and where the 'is_duplicate' dataframe has True values, it replaces them with np.nan
    a[[f"a_{i}" for i in range(0,xx)]] = a[[f"a_{i}" for i in range(0,xx)]].where(~is_duplicate, np.nan).fillna('zzzyyyy')

    # A way to change nan values to another value

    for i in range(xx):
        a[f"a_{i}"] = a[f"a_{i}"].str.strip()

    u, c = np.unique(a[[f"a_{i}" for i in range(xx)]].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.drop(['zzzyyyy'], inplace=True)
    a.reset_index(level=0, inplace=True)

        # ################################################################################
        # # Find the most common genres
        # ################################################################################
        # a["awards"] = a["awards"].str.replace(r"[^A-Za-z]", " ", regex=True)
        # a.to_csv("aaa.csv")

        #################################### Creating the specific awards


    a_len=len(a['index'].str.split("Award",expand=True).columns)
    a[[f"a_{i}" for i in range(a_len)]] = a['index'].str.split("Award",expand=True)
    a['a_0'] = a['a_0'].str.strip()
    print(len(a['a_0']))


    u, c = np.unique(a['index'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.reset_index(level=0, inplace=True)
    a_len=len(a['index'].str.split("Nominee",expand=True).columns)
    a[[f"a_{i}" for i in range(a_len)]] = a['index'].str.split("Nominee",expand=True)
    a['a_0'] = a['a_0'].str.strip()
    print(len(a['a_0']))
    u, c = np.unique(a['index'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.reset_index(level=0, inplace=True)
    a_len=len(a['index'].str.split("AAR",expand=True).columns)
    a[[f"a_{i}" for i in range(a_len)]] = a['index'].str.split("AAR",expand=True)
    a['a_0'] = a['a_0'].str.strip()
    print(len(a['a_0']))
    #
    u, c = np.unique(a['a_0'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.reset_index(level=0, inplace=True)
    a_len=len(a['index'].str.split("by",expand=True).columns)
    a[[f"a_{i}" for i in range(a_len)]] = a['index'].str.split("by",expand=True)
    a['a_0'] = a['a_0'].str.strip()
    print(len(a['a_0']))
    u, c = np.unique(a['a_0'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.reset_index(level=0, inplace=True)
    a_len=len(a['index'].str.split("de ",expand=True).columns)
    a[[f"a_{i}" for i in range(a_len)]] = a['index'].str.split("de ",expand=True)
    a['a_0'] = a['a_0'].str.strip()
    print(len(a['a_0']))
    #
    u, c = np.unique(a['a_0'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.reset_index(level=0, inplace=True)
    a_len=len(a['index'].str.split("for",expand=True).columns)
    a[[f"a_{i}" for i in range(a_len)]] = a['index'].str.split("for ",expand=True)
    a['a_0'] = a['a_0'].str.strip()
    print(len(a['a_0']))
    ### Final
    u, c = np.unique(a['a_0'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    a = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    a.sort_values('count', ascending=False)
    a.reset_index(level=0, inplace=True)


    u, c = np.unique(a['index'].values, return_counts=True)
    new_dd = dict(zip(u, c))
    final = pd.DataFrame.from_dict(new_dd, orient='index',columns=['count'])
    final.to_csv('award_categories.csv')


def genre_column_maker():
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
        #df[genre] = df[genre].map({True: 'Yes', False: 'No'})

    df.drop([f"genre_{i}" for i in range(0,20)], inplace=True, axis=1)
    df.drop(df.columns[[0,1]], axis=1, inplace=True)

    return df.to_csv("data/9745_greatest_books_ever.csv")
#genre_column_maker(dataset)


df =  pd.read_csv(dataset)


def audio_book(data):
    df = data[['Audiobook', 'good_read_score', 'original_publish_year']]

    gdf = df[df["original_publish_year"] > 2000]
