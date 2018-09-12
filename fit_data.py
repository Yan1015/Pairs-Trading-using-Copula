import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects

copula = importr('copula', lib_loc="C:/Users/zy108/Documents/R/win-library/3.5")
copBasic = importr('copBasic', lib_loc="C:/Users/zy108/Documents/R/win-library/3.5")
VineCopula = importr('VineCopula', lib_loc="C:/Users/zy108/Documents/R/win-library/3.5")

r_script = '''
library(Rsafd)
df <- read.csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/train_data_transfer_to_R.csv")
df1 <- read.csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/test_data_transfer_to_R.csv")
stock1_cumu_log_ret <- df[1]
stock2_cumu_log_ret <- df[2]

#### obtain marginals
stock1_est<-fit.gpd(stock1_cumu_log_ret, plot=FALSE)
stock2_est<-fit.gpd(stock2_cumu_log_ret, plot=FALSE)
#### compute uniforms
U<-pgpd(stock1_est,stock1_cumu_log_ret)
V<-pgpd(stock2_est,stock2_cumu_log_ret)
Fam = c(1, 2, 3, 4, 5, 6, 13, 14, 16, 23, 24, 26, 33, 34, 36)
selectedCopula = BiCopSelect(U, V, familyset=Fam)

stock1_ret_list <- df1[1]
stock2_ret_list <- df1[2]

U1<-pgpd(stock1_est,stock1_ret_list)
V1<-pgpd(stock2_est,stock2_ret_list)
'''


df = pd.read_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/daily_log_ret.csv")

train_df = df.loc[:int(len(df) * 2 / 3), :]
test_df = df.loc[int(len(df) * 2 / 3) + 1:, :]

trading_date_num = len(test_df)
trading_date_list = list(test_df['Date'])

high_corr_stocks_pairs = pd.read_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/high_corr_stocks_pairs.csv")
print(high_corr_stocks_pairs)

pair_num = len(high_corr_stocks_pairs)

columns = df.columns
stocks_list = columns[1::]

signal_df = pd.DataFrame(np.arange(trading_date_num * 1).reshape(trading_date_num, 1), index=range(trading_date_num), columns=[0])

signal_columns = []
for index in high_corr_stocks_pairs.index:
    stock1 = high_corr_stocks_pairs.loc[index, 'stock1']
    stock2 = high_corr_stocks_pairs.loc[index, 'stock2']
    df1 = train_df.loc[:, [stock1, stock2]]
    df2 = test_df.loc[:, [stock1, stock2]]
    df1.to_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/train_data_transfer_to_R.csv", index=False)
    df2.to_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/test_data_transfer_to_R.csv", index=False)

    robjects.r(r_script)

    selectedCopula = robjects.r['selectedCopula']

    family = selectedCopula[4][0]
    parameter = selectedCopula[1][0]
    AIC = selectedCopula[11][0]
    BIC = selectedCopula[12][0]
    tau = selectedCopula[5][0]  # Kendall's tau
    print(family)
    print(parameter)
    print(AIC)
    print(BIC)
    print(tau)

    u1 = robjects.r['U1']
    v1 = robjects.r['V1']

    BiCopHfunc1 = robjects.r['BiCopHfunc1']  # the probability that V ≤ v given that U = u
    BiCopHfunc2 = robjects.r['BiCopHfunc2']  # the probability that U ≤ u given that V = v

    deriv1 = BiCopHfunc1(u1, v1, selectedCopula)
    deriv2 = BiCopHfunc2(u1, v1, selectedCopula)
    # print(deriv1)
    # print(deriv2)

    deriv1 = list(deriv1)
    deriv2 = list(deriv2)

    i = 0
    signal1 = 0
    signal2 = 0
    signal_list = []


    while i < len(deriv1):
        signal_list.append(str(signal1) + '&' + str(signal2))
        deriv_num1 = deriv1[i]
        deriv_num2 = deriv2[i]
        if signal1 == 0:
            if (deriv_num1 >= 0.95) and (deriv_num2 <= 0.05):
                signal1 = 'long'
                signal2 = 'short'

            if (deriv_num1 <= 0.05) and (deriv_num2 >= 0.95):
                signal1 = 'short'
                signal2 = 'long'

        if signal1 == 'long':
            if (deriv_num1 <= 0.5) and (deriv_num2 >= 0.5):
                signal1 = 0
                signal2 = 0

        if signal1 == 'short':
            if (deriv_num1 >= 0.5) and (deriv_num2 <= 0.5):
                signal1 = 0
                signal2 = 0

        i = i + 1

    signal_df[stock1 + '&' + stock2] = signal_list
    signal_columns.append(stock1 + '&' + stock2)

signal_df['Date'] = trading_date_list
signal_df = signal_df.loc[:, ['Date'] + signal_columns]
signal_df.to_csv("C:/Users/zy108/Desktop/9743_Statidtical analysis of fin in R/project/trading_signal.csv", index=False)
