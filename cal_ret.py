import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects

df = pd.read_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/daily_log_ret.csv")

train_df = df.loc[:int(len(df) * 2 / 3), :]
test_df = df.loc[int(len(df) * 2 / 3) + 1:, :]

trading_date_num = len(test_df)
trading_date_list = list(test_df['Date'])



signal_df = pd.read_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/trading_signal.csv")
columns = signal_df.columns
columns = columns[1::]

ret_df = pd.DataFrame(np.arange(len(columns)).reshape(len(columns), 1), index=columns, columns = ['average_annual_ret'])
print(signal_df)

average_annual_ret_list = []
for item in signal_df.columns:
    if item != 'Date':
        stock1 = item.split('&')[0]
        stock2 = item.split('&')[1]
        print(stock1)
        print(stock2)
        original_list = list(signal_df[item])
        signal1_list = []
        signal2_list = []
        for i in original_list:
            signal1_list.append(i.split('&')[0])
            signal2_list.append(i.split('&')[1])

        ret1_list = list(df[stock1])
        ret2_list = list(df[stock2])

        sum1 = 0
        num1 = 0
        sum2 = 0
        num2 = 0
        for i in range(len(signal1_list)):
            if signal1_list[i] == 'short':
                num1 = num1 + 1
                sum1 = sum1 - ret1_list[i]
            if signal1_list[i] == 'long':
                num1 = num1 + 1
                sum1 = sum1 + ret1_list[i]
            if signal2_list[i] == 'short':
                num2 = num2 + 1
                sum2 = sum2 - ret2_list[i]
            if signal2_list[i] == 'long':
                num2 = num2 + 1
                sum2 = sum2 + ret2_list[i]

        if num1 != 0:
            ret1 = (sum1 / num1) *252
        else:
            ret1 = 0

        if num2 != 0:
            ret2 = (sum2 / num2) * 252
        else:
            ret2 = 0

        average_annual_ret = (ret1 * num1 + ret2 * num2) / trading_date_num
        average_annual_ret_list.append(average_annual_ret)


ret_df['average_annual_ret'] = average_annual_ret_list
print(ret_df)
ret_df.to_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/average_annual_ret.csv")
