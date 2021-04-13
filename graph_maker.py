import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/preprocess_complete.csv")



def most_reviewd_books(df):
    mostly_reviewed = df.sort_values(by='num_reviews', ascending=False) # Sorting by number of reviews
    mostly_reviewed = mostly_reviewed[['title','num_reviews']] # Selecting just the columns we want
    mostly_reviewed = mostly_reviewed.head(15) # Choosing only the top 10 books
    plt.figure(figsize=(12,5))
    sns.barplot(y='title', x='num_reviews', data = mostly_reviewed, palette="tab10")
    plt.title('15 Most Reviewed Books', fontsize='20')
    plt.xlabel('Number of Reviews (in mln.)')
    plt.ylabel('Book Title')
    return plt.show()

def plotCorrelationMatrix(df, graphWidth):
    filename = df
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    return plt.show()

def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    return plt.show()


input_dict = {
            "1": most_reviewd_books(df),
            "2": plotCorrelationMatrix(df, 8),
            "3": plotPerColumnDistribution(df, 10, 5),
            }


finished = False
viewing = None
while finished == False:
