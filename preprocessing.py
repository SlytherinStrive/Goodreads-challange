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
    print(len(df))

    df = df.dropna(subset=['num_pages'])
    df = df.dropna(subset=['avg_rating'])
    df = df.dropna(subset=['num_ratings'])
    df = df.dropna(subset=['num_reviews'])
    df = df.dropna(subset=['original_publish_year'])
    df = df.dropna(subset=['genres'])
    df = df.reset_index()
    print(df.isna().sum())
    return df.to_csv("clean_data.csv")

if __name__ == "__main__":
    load_csv = "scraped_2000.csv"
    preprocessing(load_csv)
