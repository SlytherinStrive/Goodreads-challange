import pandas as pd
import numpy as np
import re

#Normalise the min-max data and transform into a 1-10 range
def min_max_normalise(ratings):
    normalised = ((ratings - min(ratings)) / (max(ratings) - min(ratings)))
    transform = ((normalised + 1) * 4.5) + 1
    return transform

#Normalise the data and transform into a 1-10 range
def normalise_mean(ratings):
    normalised = ((ratings - np.mean(ratings)) / (max(ratings) - min(ratings)))
    transform = ((normalised + 1) * 4.5) + 1
    return transform

#Transform the number of pages from float to int
def num_page_clean(num_pages):
    for obj in num_pages:
        obj =int(round(obj))
    return (int(num_pages))

#Clean the awards data and count the number of awards
def awards_cleaned(awards):
    return (awards.str.count(r"([0-9]{4})")).replace(np.nan, 0)

def preprocessing(csv_lock):
    df = pd.read_csv(csv_lock)
    ### Clean Data
    df = df.dropna(subset=['num_pages', 'avg_rating', 'num_ratings', 'num_reviews', 'original_publish_year','genres'])
    df = df.reset_index()
    df[['num_pages', 'num_ratings', 'num_reviews']] = df[['num_pages', 'num_ratings', 'num_reviews']].astype(int)
    df[['url', 'title', 'author', 'genres', 'awards', 'place']] = df[['url', 'title', 'author', 'genres', 'awards', 'place']].astype(str)
    ### Add new columns
    df["minmax_norm_ratings"] = min_max_normalise(df['avg_rating'])
    df['normalise_mean'] = normalise_mean(df['avg_rating'])
    
    print(df.isna().sum())
    print(df.info())
    return df.to_csv(f"data/preprocess_complete_.csv")
