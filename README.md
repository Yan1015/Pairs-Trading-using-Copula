# Pairs-Trading-using-Copula
## Introdution
This project is to apply Copula Function to pair trading strategy in American stock market by Python and R. I using the package rpy2.robjects in Python to help me run the R code in Python environment because I can combine the benefit of Pyhton and R together. Python does better on big data and R is good for applying copula approach.
#### Copula
In statistics, a copula function is a multivariate probability distribution for which the marginal probability distribution of each variable is uniform. Copulas are used to describe the dependence between random variables.
#### Pairs Trading
The objective of pairs trading is to identify the relative overvalued and undervalued positions between two stocks that are closely related, with a long-run relationship. 

Such relative mispricing occurs if the spread between the two stocks deviates from its equilibrium, and excess returns will be generated if the pair is mean-reverting (that is, any deviations are temporary, and will return to its equilibrium after a period of adjustment). In this situation, the strategy will simultaneously short the relatively overvalued stock and long the relatively undervalued. 

Therefore, the most important part is the identify the relative  overvalued stock and the undervalued stock. That’s what copula can help us.
## Data and Pairs selecting
I downloaded the all the 505 stocks' daily close price in S&P 500 index from Bloomberg form 2008 to 2018. And after calculating the log-retrun, I tested the correlation for all the stocks pairs and selected the pairs whose absolute correlation is greater than 0.85.
## Data fitting
For each selected stock pairs, Calculate the marginal distributions by the R function fit.gpd
