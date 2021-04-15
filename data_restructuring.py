import pandas as pd
import numpy as np
import glob
import datetime as dt


def csv_merger(new_filename, path=r'combinefiles/data', date_include=True):
    # Checks new file name is a string
    if isinstance(new_filename, str):
        ## Gathers all csv's in specified path
        all_files = glob.glob(path + "/*.csv")
        list_of_csv = []
        ## Append all files into a python list
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            list_of_csv.append(df)

        ## Create a dateframe concatenating all CSV's
        df = pd.concat(list_of_csv, axis=0, ignore_index=True)

        ## Export all Combined CSV's to directory
        if date_include == True:
            date_insert = "_" + "".join([num for num in str(dt.date.today()) if num.isnumeric()])
            df.to_csv("data/"+new_filename+date_insert+".csv", index=False, header=True)
            print("Merge succuessful")
        elif date_include == False:
            df.to_csv("data/"+new_filename+".csv", index=False, header=True)
            print("Merge succuessful")
        else:
            print("Invalid argument for date_include. Must be True or False")
    else:
        print("Invalid new file name - must be type(str)")


def merge_data_dicts(list_of_dictionaries):
    all_data = {}
    for dict in list_of_dictionaries:
        for key, value in dict.items():
            if key in all_data.keys():
                current_data = all_data[key]
                combined_data = current_data + value
                all_data[key] = combined_data
            else:
                all_data[key] = value
    return all_data


csv_merger("15th_1k", path='data/data15th',date_include=False)
