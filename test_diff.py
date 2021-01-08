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
import M_intraday_data as mid
import M_buy_sell_routine as bsr
import numpy as np
import csv

# Basic initialization
time_steps = 30 # Minimum number of time data required
c = time_steps - 1 # Recent price index
style.use("ggplot")


def write_csv(data, file):
    with open(file, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


def read_csv(file):
    df = pd.read_csv(file, index_col=False)
    return df


def find_diff():
    for ticker in tickers:       
        datafile = 'Intraday_stock_data/{}.csv'.format(ticker)
        df = read_csv(datafile)
        df_temp = np.array(df['CLOSE'], dtype = float)
        df_temp1 = np.array(df['Datetime'], dtype = object)
    
        for i in range(time_steps, len(df_temp)):
            df_current = df_temp[(i - time_steps):i]
            df_time = df_temp1[(i - time_steps):i] 
            price = df_current[c]
            time = df_time[c]
            loc_avg = sum(df_current[:-1]) / (len(df_current) - 1)
            diff = (df_current[c] - loc_avg) / loc_avg
            variance = pow((df_current[c] - loc_avg), 2) / time_steps
            std_dev = np.sqrt(variance)
            write_csv([time, price, diff, variance, std_dev],
                      'stocks_diff/{}_diff.csv'.format(ticker))


tickers = mid.get_tickers()
if not os.path.exists('stocks_diff'):
        os.makedirs('stocks_diff')
find_diff()
for tick in tickers:
    path = os.getcwd() + '/stocks_diff/{}_diff.csv'.format(tick)
    bsr.load_bsr(tick, path, 'diff')
