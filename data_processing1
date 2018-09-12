import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

df1 = pd.read_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/SP500_2008-2018.csv")
columns = list(df1.columns)
columns[0] = "Date"
df1.columns = columns
stocks_list = columns[1::]
date_list = list(df1['Date'])

a = date_list.index('5/1/2015')
print(a)

df1 = df1.loc[a:len(df1), :]
df1.index = list(range(len(df1)))

for stock in stocks_list:
    print(stock)
    df1[stock + 'lag_1'] = df1[stock].shift(1).fillna(1)
    df1[stock + '_log_ret'] = df1.apply(lambda x: math.log(x[stock] / x[stock + 'lag_1']), axis=1)

log_ret_column_list = []
for stock in stocks_list:
    log_ret_column_list.append(stock + '_log_ret')

df = df1.loc[:, ['Date'] + log_ret_column_list]
df.columns = ['Date'] + stocks_list
date_list = list(df['Date'])
df.index = list(range(len(df)))
df = df.loc[1:len(df), :]
df.to_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/daily_log_ret.csv", index=False)
