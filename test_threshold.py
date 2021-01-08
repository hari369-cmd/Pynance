import bs4 as bs
import pickle
import re
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import csv
import M_intraday_data as mid
import M_buy_sell_routine as bsr

# Basic initialization
time_steps = 30 # Minimum number of time data required
c = time_steps - 1 # Recent price index
counter = -1 # Counter for number of times data is obtained (Selenium)
style.use("ggplot")

min_per_change = 0.07 # Minimum percentage change of stock price


def write_csv(data, file):
    with open(file, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)



def read_csv(file):
    df = pd.read_csv(file, index_col=False)
    return df



def moving_average(df_current, counter, diff):
    
    df_ma = pd.DataFrame(df_current)
    
    df_7ma = df_ma.rolling(window = 7, min_periods = 0).mean()
    df_15ma = df_ma.rolling(window = 15, min_periods = 0).mean()
    df_30ma = df_ma.rolling(window = 30, min_periods = 0).mean()
    
    weight_1 = 1
    weight_2 = 0
    weight_3 = 0.5
    weight_4 = 0.15
    
    if (df_7ma.iloc[c].values < df_15ma.iloc[c].values):
        
        if (diff <= 0):
            return -weight_1
        elif (diff == 0):
            return -weight_3
        else:
            return weight_4
        
    if (df_7ma.iloc[c].values == df_15ma.iloc[c].values):
        
        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_2
        else:
            return weight_3
        
    if (df_7ma.iloc[c].values > df_15ma.iloc[c].values):

        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_3
        else:
            return weight_1

        

def exp_moving_average(df_current, counter, diff):

    df_ema = pd.DataFrame(df_current)
    
    df_7ema = df_ema.ewm(span = 7, min_periods = 0).mean()
    df_12ema = df_ema.ewm(span = 12, min_periods = 0).mean()
    df_15ema = df_ema.ewm(span = 15, min_periods = 0).mean()
    df_26ema = df_ema.ewm(span = 26, min_periods = 0).mean()
    df_30ema = df_ema.ewm(span = 30, min_periods = 0).mean()

    weight_1 = 1
    weight_2 = 0
    weight_3 = 0.5
    weight_4 = 0.15
    
    if (df_7ema.iloc[c].values < df_15ema.iloc[c].values):
        
        if (diff < 0):
            return -weight_1
        elif (diff == 0):
            return -weight_3
        else:
            return weight_4
        
    elif (df_7ema.iloc[c].values == df_15ema.iloc[c].values):

        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_2
        else:
            return weight_3
        
    elif (df_7ema.iloc[c].values > df_15ema.iloc[c].values):

        if (diff < 0):
            return -weight_4
        elif (diff == 0):
            return weight_3
        else:
            return weight_1

        

def MACD(df_current, counter, diff):

    df_ema = pd.DataFrame(df_current)

    df_12ema = df_ema.ewm(span = 12, min_periods = 0).mean()
    df_26ema = df_ema.ewm(span = 26, min_periods = 0).mean()

    MACD = df_12ema - df_26ema
    signal = MACD.ewm(span = 9, min_periods = 0).mean()

    weight_1 = 1
    weight_2 = 0
    weight_3 = 0.5
    weight_4 = 0.15
    
    if (MACD.iloc[c].values < signal.iloc[c].values):

        if (diff < 0):
            return -weight_1
        elif (diff == 0):
            return -weight_3
        else:
            return weight_4
        
    elif (MACD.iloc[c].values == signal.iloc[c].values):

        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_2
        else:
            return weight_3
        
    elif (MACD.iloc[c].values > signal.iloc[c].values):

        if (diff < 0):
            return -weight_4
        elif (diff == 0):
            return weight_3
        else:
            return weight_1

        

def bol_bands(df_current, counter):

    df_ma = pd.DataFrame(df_current)
    recent_price = df_current[c]

    df_7ma = df_ma.rolling(window = 7, min_periods = 0).mean()
    df_7std = df_ma.rolling(window = 7, min_periods = 0).std()

    Upper = df_7ma.iloc[c].values + (df_7std.iloc[c].values * 2)
    Lower = df_7ma.iloc[c].values - (df_7std.iloc[c].values * 2)

    if (recent_price < Lower):
        return -1
    elif (recent_price >= Lower and recent_price <= Upper):
        return 0
    elif (recent_price > Upper):
        return 1



def rel_strength_index(df_current, counter):

    UP = 70
    LOW = 30
    df_high = []
    df_low = []

    recent_price = df_current[c]

    for j in range(0, len(df_current), 1):
        if(df_current[j] > recent_price):
            df_high.append(df_current[j])
        elif(df_current[j] < recent_price):
            df_low.append(df_current[j])
        else:
            continue
    
    if (len(df_high) == 0):
      df_high.append(0)
    if (len(df_low) == 0):
      df_low.append(0)
      
    avg_high = sum(df_high) / len(df_high)
    avg_low = sum(df_low) / len(df_low)

    if (avg_low == 0):
        avg_low = 1
    RS = avg_high / avg_low
    RSI = 100 - (100 / (1 + RS)) # RSI values lie between 0 to 100
    
    if (RSI < LOW):
        return 1
    elif (RSI >= LOW and RSI <= UP):
        return 0
    elif (RSI > UP):
        return -1

    

def comm_chann_index(df_current, counter):

    CONST = 0.015
    UP = 70
    LOW = 10

    df_ma = pd.DataFrame(df_current)
    recent_price = df_current[c]

    df_max = max(df_current)
    df_min = min(df_current)

    df_25ma = df_ma.rolling(window = 25, min_periods = 0).mean()
    df_25ma_std = df_ma.rolling(window = 25, min_periods = 0).std()
    
    if (df_25ma_std.iloc[c].values == 0):
        df_25ma_std.iloc[c].values = 1 

        
    TP = (df_max + df_min + recent_price) / 3
    CCI = (TP - df_25ma.iloc[c].values) / (CONST * df_25ma_std.iloc[c].values) # returns values between -100 to 100
    
    if (CCI < LOW):
        return 1
    elif (CCI >= LOW and CCI <= UP):
        return 0
    elif (CCI > UP):
        return -1



def stoch_oscillator(df_current, counter):

    UP = 70
    LOW = 30

    recent_price = df_current[c]
    
    df_max = max(df_current)
    df_min = min(df_current)
    denominator = df_max - df_min

    if (denominator == 0):
        denominator = 1
    
    # K returns values between 0 to 100
    K = ((recent_price - df_min) / denominator) * 100
    
    if (K < LOW):
        return 1
    elif (K >= LOW and K <= UP):
        return 0
    elif (K > UP):
        return -1



def find_threshold(tickers):
    for datafile in tickers:        
        df = read_csv('Intraday_stock_data/{}.csv'.format(datafile))
        df_temp = np.array(df['CLOSE'], dtype = float)
        df_temp1 = np.array(df['Datetime'], dtype = object)
        print(datafile)
        
        for i in range(time_steps, len(df_temp)):
            df_current = df_temp[(i - time_steps):i]
            df_time = df_temp1[(i - time_steps):i] 
            price = df_current[c]
            time = df_time[c]
            loc_avg = sum(df_current[:-1]) / (len(df_current) - 1)
            diff = (df_current[c] - loc_avg) / loc_avg
            variance = pow((df_current[c] - loc_avg), 2) / time_steps
            std_dev = np.sqrt(variance)
            if (diff <= 0):
                diff = -1
            elif (diff > 0 and diff <= min_per_change):
                diff = 0
            else:
                diff = 1
        
            counter = 0
            # Technical indicators
            ma = moving_average(df_current, counter, diff)
            ema = exp_moving_average(df_current, counter, diff)
            macd = MACD(df_current, counter, diff)
            bb = bol_bands(df_current, counter)
            rsi = rel_strength_index(df_current, counter)
            cci = comm_chann_index(df_current, counter)
            so = stoch_oscillator(df_current, counter)

            # Average
            threshold = (ma + ema + macd + bb + rsi + cci + so) / 7
            write_csv([time, price, threshold, variance, std_dev],
                      'stocks_threshold/{}_threshold.csv'.format(datafile))


tickers = mid.get_tickers()
if not os.path.exists('stocks_threshold'):
        os.makedirs('stocks_threshold')
find_threshold(tickers)
for tick in tickers:
    path = os.getcwd() + '/stocks_threshold/{}_threshold.csv'.format(tick)
    bsr.load_bsr(tick, path, 'threshold')
