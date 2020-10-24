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
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Basic initialization
time_steps = 60 # Minimum number of time data required
c = time_steps - 1 # Recent price index
counter = -1 # Counter for number of times data is obtained (Selenium)
style.use("ggplot")

# Choose the method of initialization
LIVE = 0 # 1-Obtain data live, 0-Use pre-existing data (check get_data)

# For pre-existing data or for long data intervals
get_data = 0 # 1-Obtain past data, 0-Use saved data
ticker = 'GC=F' # Stock ticker
start = dt.datetime(2020, 3, 1) # Start time for data from Yahoo
end = dt.datetime(2020, 7, 29) # End time for data from Yahoo
min_per_change = 0.03 # Minimum percentage change of stock price

# Choose the method of initialization
LIVE = 1 # 1-Obtain data live, 0-Use pre-existing data
datafile = '{}.csv'.format(ticker) # The pre-existing datafile or this will be the name of the datafile downloaded if get_data = 1



def write_csv(data):
    with open(datafile, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)



def read_csv():
    df = pd.read_csv(datafile, index_col=False)
    return df



def moving_average(df_current, counter, diff):
    
    df_ma = df_current
    
    df_7ma = df_ma.rolling(window = 7, min_periods = 0).mean()
    df_15ma = df_ma.rolling(window = 15, min_periods = 0).mean()
    df_30ma = df_ma.rolling(window = 30, min_periods = 0).mean()
    
    weight_1 = 1
    weight_2 = 0
    weight_3 = 0.5
    weight_4 = 0.15
    
    if (df_7ma.iloc[c] < df_15ma.iloc[c]):
        
        if (diff <= 0):
            return -weight_1
        elif (diff == 0):
            return -weight_3
        else:
            return weight_4
        
    if (df_7ma.iloc[c] == df_15ma.iloc[c]):
        
        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_2
        else:
            return weight_3
        
    if (df_7ma.iloc[c] > df_15ma.iloc[c]):

        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_3
        else:
            return weight_1

        

def exp_moving_average(df_current, counter, diff):

    df_ema = df_current
    
    df_7ema = df_ema.ewm(span = 7, min_periods = 0).mean()
    df_12ema = df_ema.ewm(span = 12, min_periods = 0).mean()
    df_15ema = df_ema.ewm(span = 15, min_periods = 0).mean()
    df_26ema = df_ema.ewm(span = 26, min_periods = 0).mean()
    df_30ema = df_ema.ewm(span = 30, min_periods = 0).mean()

    weight_1 = 1
    weight_2 = 0
    weight_3 = 0.5
    weight_4 = 0.15
    
    if (df_7ema.iloc[c] < df_15ema.iloc[c]):
        
        if (diff < 0):
            return -weight_1
        elif (diff == 0):
            return -weight_3
        else:
            return weight_4
        
    elif (df_7ema.iloc[c] == df_15ema.iloc[c]):

        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_2
        else:
            return weight_3
        
    elif (df_7ema.iloc[c] > df_15ema.iloc[c]):

        if (diff < 0):
            return -weight_4
        elif (diff == 0):
            return weight_3
        else:
            return weight_1

        

def MACD(df_current, counter, diff):

    df_ema = df_current

    df_12ema = df_ema.ewm(span = 12, min_periods = 0).mean()
    df_26ema = df_ema.ewm(span = 26, min_periods = 0).mean()

    MACD = df_12ema - df_26ema
    signal = MACD.ewm(span = 9, min_periods = 0).mean()

    weight_1 = 1
    weight_2 = 0
    weight_3 = 0.5
    weight_4 = 0.15
    
    if (MACD.iloc[c] < signal.iloc[c]):

        if (diff < 0):
            return -weight_1
        elif (diff == 0):
            return -weight_3
        else:
            return weight_4
        
    elif (MACD.iloc[c] == signal.iloc[c]):

        if (diff < 0):
            return -weight_3
        elif (diff == 0):
            return weight_2
        else:
            return weight_3
        
    elif (MACD.iloc[c] > signal.iloc[c]):

        if (diff < 0):
            return -weight_4
        elif (diff == 0):
            return weight_3
        else:
            return weight_1

        

def bol_bands(df_current, counter):

    df_ma = df_current
    recent_price = df_current.iloc[c]

    df_7ma = df_ma.rolling(window = 7, min_periods = 0).mean()
    df_7std = df_ma.rolling(window = 7, min_periods = 0).std()

    Upper = df_7ma.iloc[c] + (df_7std.iloc[c] * 2)
    Lower = df_7ma.iloc[c] - (df_7std.iloc[c] * 2)

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

    recent_price = df_current.iloc[c]

    for j in range(0, len(df_current), 1):
        if(df_current.iloc[j] > recent_price):
            df_high.append(df_current.iloc[j])
        elif(df_current.iloc[j] < recent_price):
            df_low.append(df_current.iloc[j])
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

    df_ma = df_current
    recent_price = df_current.iloc[c]

    df_max = max(df_current)
    df_min = min(df_current)

    df_25ma = df_ma.rolling(window = 25, min_periods = 0).mean()
    df_25ma_std = df_ma.rolling(window = 25, min_periods = 0).std()
    
    if (df_25ma_std.iloc[c] == 0):
        df_25ma_std.iloc[c] = 1 

    if (df_25ma_std.iloc[c] == 0):
        df_25ma_std.iloc[c] = 1
        
    TP = (df_max + df_min + recent_price) / 3
    CCI = (TP - df_25ma.iloc[c]) / (CONST * df_25ma_std.iloc[c]) # returns values between -100 to 100

    if (CCI < LOW):
        return 1
    elif (CCI >= LOW and CCI <= UP):
        return 0
    elif (CCI > UP):
        return -1



def stoch_oscillator(df_current, counter):

    UP = 70
    LOW = 30

    recent_price = df_current.iloc[c]
    
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


driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://goldprice.org/")
i = 1
for i in range(100):
    sleep(1)
    price = driver.find_element_by_xpath('//*[@id="gpxtickerLeft_price"]').text
    price = float(price.replace(",",""))

    i +=1


    if (LIVE == 1):
        # The following code should be inside the Selenium's "for" loop
        counter += 1
        time = dt.datetime.now()

        if(counter < time_steps):
            write_csv([time, price])

        if(counter > time_steps):
            write_csv([time, price])
            df = read_csv()
            # Obtain the min. number of time period data and save it in df_current
            df_temp = df[(len(df) - time_steps):]
            #Changed for only prices
            #df_temp.columns = ['date','price']
            #df_temp = df_temp.drop(columns='date')
            df_temp.drop(df.columns[0], 1, inplace=True)
            #df_current = pd.Series(df_temp['price'])
            df_current = df_temp.iloc[:,0]


            if (len(df_current) < time_steps):
                print("Time steps greater than number of periods of data")

            loc_avg = sum(df_current)/ len(df_current)
            diff = (df_current.iloc[c] - loc_avg) / 100
            if (diff <= 0):
                diff = -1
            elif (diff > 0 and diff <= min_per_change):
                diff = 0
            else:
                diff = 1

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
            # print(threshold)
            print(threshold, ma, ema, macd, bb, rsi, cci, so)

            # Activation condition
            # Code above should be inside the Selenium's "for" loop

    else:
        if(get_data == 1):
            df_web = web.get_data_yahoo(ticker, start, end)
            df_web.to_csv(datafile)
            
        df = read_csv()
        df.drop(["Date","Open","High","Low","Close","Volume"], 1, inplace=True)
        df_temp = df[(len(df) - time_steps):]
        df_current = df_temp.iloc[:,0]
    
        if (len(df_current) < time_steps):
            if (len(df_current) == 0):
                print("Input data set is empty. Check the csv file")
                exit()
            print("Time steps greater than number of periods of data")

        loc_avg = sum(df_current) / len(df_current) 
        diff = (df_current.iloc[c] - loc_avg) / 100
        if (diff <= 0):
            diff = -1
        elif (diff > 0 and diff <= min_per_change):
            diff = 0
        else:
            diff = 1
        
        counter = 0 # Not applicable for offline data
        
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
        print(threshold)
