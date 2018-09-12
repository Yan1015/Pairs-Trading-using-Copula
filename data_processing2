import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

df = pd.read_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/daily_log_ret.csv")
high_corr_stocks_pairs = pd.DataFrame(np.arange(2).reshape(1, 2), index=[0], columns = ['stock1', 'stock2'])
print(df)
columns = df.columns
stocks_list = columns[1::]
df1 = df.loc[:, stocks_list]

corr_matrix = df1.corr()
pair_num = 0
for i in range(len(stocks_list)):
    stock = stocks_list[i]
    corr_list = list(corr_matrix[stock])
    for j in range(len(corr_list)):
        if corr_list[j] >= 0.85:
            if j > i:
                high_corr_stocks_pairs.loc[pair_num, 'stock1'] = stocks_list[i]
                high_corr_stocks_pairs.loc[pair_num, 'stock2'] = stocks_list[j]
                pair_num = pair_num + 1

print(high_corr_stocks_pairs)
print(len(high_corr_stocks_pairs))
high_corr_stocks_pairs.to_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/high_corr_stocks_pairs.csv", index=False)

