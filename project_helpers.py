import requests
import pandas as pd
import numpy as np
import glob

# df = pd.concat(
# combined_csv_data = pd.concat([pd.read_csv(f, delimiter='t', encoding='UTF-16')

# print(df.head())
# import pandas as pd
# import glob

path = r'data/combinefiles' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

df.to_csv('scraped_2000.csv',index = False, header=True)
