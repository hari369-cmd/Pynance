import yfinance as yf, pandas as pd, shutil, os, time, glob
import numpy as np
import requests
from get_all_tickers import get_tickers as gt
from statistics import mean
import talib
import matplotlib.pyplot as plt

"""
Working of RSI
- Observe the last 14 closing prices of a stock.
- Determine whether the current time period's closing price is higher or lower than the previous one.
- Calculate the average gain and loss over the last 14 time period's.
- Compute the relative strength (RS): (AvgGain/AvgLoss)
- Compute the relative strength index (RSI): (100–100 / ( 1 + RS))

Working with smoothed RSI
- https://mrjbq7.github.io/ta-lib/doc_index.html
- Compute the relative strength (RS): EMA smoothed
"""


# Get the path for each stock file in a list
list_files = (glob.glob("/Users/ks/bot/Pynance/yfinance/stock_data_min/*.csv"))

# Create the dataframe that we will be adding the final analysis of each stock to
compare_stocks = pd.DataFrame(columns=["Company", "Periods_Observed", "Crosses", "True_Positive", "False_Positive", "True_Negative", "False_Negative", "Sensitivity", 
"Specificity", "Accuracy", "TPR", "FPR"])

# loop to cycle through the stocks 
for stock in list_files:
    # Dataframe to hold the historical data of the stock we are interested in.
    hist_data = pd.read_csv(stock)
    # Name of company
    company = ((os.path.basename(stock)).split(".csv")[0]) 
    # Append the closing prices of a stock in prices list
    prices = []
    c = 0
    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    while c < len(hist_data):
        if hist_data.iloc[c,4] > float(2.00):
            prices.append(hist_data.iloc[c,4])
        c += 1
    # prices_df = pd.DataFrame(prices)  # Make a dataframe from the prices list
    i = 0
    up_prices=[]
    down_prices=[]
    #  Loop to hold up and down price difference 
    while i < len(prices):
        if i == 0:
            up_prices.append(0)
            down_prices.append(0)
        else:
            if (prices[i]-prices[i-1])>0:
                up_prices.append(prices[i]-prices[i-1])
                down_prices.append(0)
            else:
                down_prices.append(prices[i]-prices[i-1])
                up_prices.append(0)
        i += 1

    x = 0
    avg_gain = []
    avg_loss = []
    #  Loop to calculate the average gain and loss
    while x < len(up_prices):
        if x < 15:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sum_gain = 0
            sum_loss = 0
            y = x-14
            while y < x:
                sum_gain += up_prices[y]
                sum_loss += down_prices[y]
                y += 1
            avg_gain.append(sum_gain/14)
            avg_loss.append(abs(sum_loss/14))
        x += 1

    p = 0
    RS = []
    RSI = []
    #  Loop to calculate RSI and RS
    while p < len(prices):
        if p <15:
            RS.append(0)
            RSI.append(0)
        else:
            RSvalue = (avg_gain[p]/avg_loss[p])
            RS.append(RSvalue)
            RSI.append(100 - (100/(1+RSvalue)))
        p+=1

    RSI_smoothed = talib.RSI(hist_data['Close'], timeperiod=14)
    

    #  Creates the csv for each stock's RSI and price movements
    df_dict = {
        'Prices' : prices,
        'upPrices' : up_prices,
        'downPrices' : down_prices,
        'AvgGain' : avg_gain,
        'AvgLoss' : avg_loss,
        'RS' : RS,
        'RSI' : RSI,
        'RSI_smoothed' : RSI_smoothed
    }
    df = pd.DataFrame(df_dict, columns = ['Prices', 'upPrices', 'downPrices', 'AvgGain','AvgLoss', 'RS', "RSI", "RSI_smoothed"])
    df.to_csv("/Users/ks/bot/Pynance/rsi/rsi_data/"+company+"_RSI.csv", index = False)

    """
    Code to test the accuracy of the RSI at predicting stock prices
    -Initialize the variables we are using to measure accuracy.
    -Loop through each time period in a stocks historical data and see if the RSI crossed over the 30% or 70% line.
    -If a crossover did occur, check if the stock’s future price moved as expected.
    -Compute the measurement variables.
    -Save the accuracy measurements for each stock to the same CSV file for easy comparison.
    """

    Days_Observed = 15
    Crosses = 0
    nothing = 0
    True_Positive = 0
    False_Positive = 0
    True_Negative = 0
    False_Negative = 0
    Sensitivity = 0
    Specificity = 0
    Accuracy = 0
    while Days_Observed < len(prices)-5:
        if RSI[Days_Observed] <= 30:
            if ((prices[Days_Observed + 1] + prices[Days_Observed + 2] + prices[Days_Observed + 3] + prices[Days_Observed + 4] + prices[Days_Observed + 5])/5) > prices[Days_Observed]:
                True_Positive += 1
            else:
                False_Negative += 1
            Crosses += 1
        elif RSI[Days_Observed] >= 70:
            if ((prices[Days_Observed + 1] + prices[Days_Observed + 2] + prices[Days_Observed + 3] + prices[Days_Observed + 4] + prices[Days_Observed + 5])/5) <= prices[Days_Observed]:
                True_Negative += 1
            else:
                False_Positive += 1
            Crosses += 1
        else:
            #Do nothing
            nothing+=1
        Days_Observed += 1

    try:
        Sensitivity = (True_Positive / (True_Positive + False_Negative)) 
    except ZeroDivisionError: 
        Sensitivity = 0
    try:
        Specificity = (True_Negative / (True_Negative + False_Positive)) 
    except ZeroDivisionError:
        Specificity = 0
    try:
        Accuracy = (True_Positive + True_Negative) / (True_Negative + True_Positive + False_Positive + False_Negative) 
    except ZeroDivisionError:
        Accuracy = 0

    # Calculate the true positive rate
    TPR = Sensitivity  
    # Calculate the false positive rate
    FPR = 1 - Specificity  

    # Create a row to add to the compare_stocks
    add_row = {'Company' : company, 'Days_Observed' : Days_Observed, 'Crosses' : Crosses, 'True_Positive' : True_Positive, 'False_Positive' : False_Positive, 
    'True_Negative' : True_Negative, 'False_Negative' : False_Negative, 'Sensitivity' : Sensitivity, 'Specificity' : Specificity, 'Accuracy' : Accuracy, 'TPR' : TPR, 'FPR' : FPR}

    # Add the analysis on the stock to the existing Compare_Stocks dataframe
    compare_stocks = compare_stocks.append(add_row, ignore_index = True) 
compare_stocks.to_csv("/Users/ks/bot/Pynance/rsi/rsi_power/stock_analysis.csv", index = False)  