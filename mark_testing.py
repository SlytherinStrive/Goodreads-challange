import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler


ten_thousand = 'data/10k_books_20210414'
df = pd.read_csv('data/10k_books_20210414')


preprocessing(ten_thousand)
