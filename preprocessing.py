import pandas as pd
import numpy as np
import re

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

#Calculate the normalized ratings
def new_ratings(df):
    df["mean_norm_ratings"] = normalise_mean(df.avg_rating)

def preprocessing(csv_lock):
    df = pd.read_csv(csv_lock)
    df = df.num_pages.dropna()
    df = df.avg_rating.dropna()
    df = df.num_ratings.dropna()
    df = df.num_reviews.dropna()
    df = df.original_publish_year.dropna()
    df = df.reset_index(drop=True)

    df.num_pages = num_page_clean(df.num_pages)
    new_ratings(df)
    return df.to_csv("clean_data.csv")

if __name__ == "__main__":
    load_csv = "scraped_1000.csv"
    preprocessing(load_csv)