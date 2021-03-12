import yfinance as yf, pandas as pd, shutil, os, time, glob
import numpy as np
import requests
from get_all_tickers import get_tickers as gt
from statistics import mean
import talib
import matplotlib.pyplot as plt
import seaborn as sns 


# Get the path for each stock file in a list
list_files = (glob.glob("/Users/ks/bot/Pynance/yfinance/stock_data_min/*.csv"))



"""-TODO: Trend analysis/ volitility / variance / volume in data is important for Fibonacci """

def indicator_rsi(stock, time_period=14):
    """
    Working of RSI
    - Observe the last 14 closing prices of a stock.
    - Determine whether the current time period's closing price is higher or lower than the previous one.
    - Calculate the average gain and loss over the last 14 time period's.
    - Compute the relative strength (RS): (AvgGain/AvgLoss)
    - Compute the relative strength index (RSI): (100–100 / ( 1 + RS))
    - TODO: time_period is variable (Neural network)

    Working with smoothed RSI
    - https://mrjbq7.github.io/ta-lib/doc_index.html
    - Compute the relative strength (RS): EMA smoothed
    """

    # Create the dataframe that we will be adding the final analysis of each stock to
    rsi_power = pd.DataFrame(columns=["Company", "Periods_Observed", "Crosses", "True_Positive", "False_Positive", "True_Negative", "False_Negative", "Sensitivity", "Specificity", "Accuracy", "TPR", "FPR"])
    
    # Dataframe to hold the historical data of the stock we are interested in.
    hist_data = pd.read_csv("/Users/ks/bot/Pynance/yfinance/stock_data_min/"+stock.upper()+".csv")
    # Name of company
    company = stock
    # Append the closing prices of a stock in prices list
    prices = []
    c = 0
    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    while c < len(hist_data):
        if hist_data.iloc[c,4] > float(2.00):
            prices.append(hist_data.iloc[c,4])
        c += 1

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
        if x < time_period+1:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sum_gain = 0
            sum_loss = 0
            y = x-time_period
            while y < x:
                sum_gain += up_prices[y]
                sum_loss += down_prices[y]
                y += 1
            avg_gain.append(sum_gain/time_period)
            avg_loss.append(abs(sum_loss/time_period))
        x += 1

    p = 0
    RS = []
    RSI = []
    #  Loop to calculate RSI and RS
    while p < len(prices):
        if p <time_period+1:
            RS.append(0)
            RSI.append(0)
        else:
            RSvalue = (avg_gain[p]/avg_loss[p])
            RS.append(RSvalue)
            RSI.append(100 - (100/(1+RSvalue)))
        p+=1

    #RSI_smoothed calculation
    RSI_smoothed = talib.RSI(hist_data['Close'], timeperiod=time_period)

    
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

    df_rsi = pd.DataFrame(df_dict, columns = ['Prices', 'upPrices', 'downPrices', 'AvgGain','AvgLoss', 'RS', "RSI", "RSI_smoothed"])
    # df.to_csv("/Users/ks/bot/Pynance/rsi/rsi_data/"+company+"_RSI.csv", index = False)

    """
    Code to test the accuracy of the RSI at predicting stock prices
    -Initialize the variables we are using to measure accuracy.
    -Loop through each time period in a stocks historical data and see if the RSI crossed over the 30% or 70% line.
    -If a crossover did occur, check if the stock’s future price moved as expected.
    -Compute the measurement variables.
    """

    Days_Observed = time_period + 1
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
    add_row = {'Company' : company, 'Periods_Observed' : Days_Observed, 'Crosses' : Crosses, 'True_Positive' : True_Positive, 'False_Positive' : False_Positive, 
    'True_Negative' : True_Negative, 'False_Negative' : False_Negative, 'Sensitivity' : Sensitivity, 'Specificity' : Specificity, 'Accuracy' : Accuracy, 'TPR' : TPR, 'FPR' : FPR}

    # Add the analysis on the stock to the existing Compare_Stocks dataframe
    df_rsi_power = rsi_power.append(add_row, ignore_index = True) 
    # compare_stocks.to_csv("/Users/ks/bot/Pynance/rsi/rsi_power/stock_analysis.csv", index = False)  

    return df_rsi, df_rsi_power


def indicator_bbands(stock, time_period=21):

    """
    - TODO: time_period is variable (Neural network)
    - TODO: slope of all bands --> 0 sell signal and vv. 
    - Use BBands with diff for slope
    """
    # Dataframe to hold the historical data of the stock we are interested in.
    hist_data = pd.read_csv("/Users/ks/bot/Pynance/yfinance/stock_data_min/"+stock.upper()+".csv")
    # Name of company
    company = stock

    # Append the closing prices of a stock in prices list
    prices = []
    c = 0
    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    while c < len(hist_data):
        if hist_data.iloc[c,4] > float(2.00):
            prices.append(hist_data.iloc[c,4])
        c += 1

    upperband, middleband, lowerband = talib.BBANDS(hist_data['Close'], timeperiod=time_period, nbdevup=2, nbdevdn=2, matype=0)
    upperband_ema, middleband_ema, lowerband_ema = talib.BBANDS(hist_data['Close'], timeperiod=time_period, nbdevup=2, nbdevdn=2, matype=talib.MA_Type.T3)
    
    #  Creates the csv for each stock's bbands
    df_dict = {
        'Company' : company,
        'Prices' : prices,
        'upperband' : upperband,
        'lowerband' : lowerband,
        'middleband' : middleband,
        'upperband_ema' : upperband_ema,
        'lowerband_ema' : lowerband_ema,
        'middleband_ema' : middleband_ema,
    }

    df_bbands = pd.DataFrame(df_dict, columns = ['Company', 'Prices', 'upperband', 'lowerband', 'middleband','upperband_ema', 'lowerband_ema', "middleband_ema"])

    return df_bbands

def plots():
    stock = input('Enter Stock symbol: ')
    time_period = input('Enter desired time period for indicator: ')
    df_rsi, df_rsi_power = indicator_rsi(stock, time_period)
    df_bbands = indicator_bbands(stock, time_period)



if __name__ == '__main__':
    plots()