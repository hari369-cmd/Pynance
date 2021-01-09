import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#plt.style.use('ggplot')

file = 'Data/data_5_nov.csv'

def read_csv(file):
    df = pd.read_csv(file, index_col=False)
    return df

indicators = ['Stock price']

len1 = 2
len2 = 2
df = read_csv(file)
df.columns = ['Date', 'Price', 'MA', 'EMA', 'MACD', 'BB', 'RSI', 'CCI', 'SO', 'Threshold']
temp = range(0, len(df['Date']), 1)
threshold = df['Threshold']

tot_buy = 16
start_sell = 8
buy = []
buy_time = []
sell = []
sell_time = []
gain = []
var = []

min_threshold = -0.3
max_threshold = 0.2
sell_percent = 0.001
price_drop_percent = 0.008
profit_percent = 0.008
# count = 0
buy_count = 0

def buy_routine(price, time):
    buy.append(price)
    buy_time.append(time)

def additional_buy_routine(price, time, index):
    buy[index] = price
    buy_time[index] = time
    
def sell_routine(price, time, min_buy):
    sell.append(price)
    gain.append(price - min_buy)
    sell_time.append(time)


for i in range(0, len(df['Price'])):

    # Selling any buys with sufficient profits
    for j in range(0, len(buy)):
        profitable_target = buy[j] + (buy[j] * profit_percent)
        if (df['Price'][i] >= profitable_target):
            sell_routine(df['Price'][i], df['Date'][i], buy[j])
            var.append(j)
    # Remove buys that were sold
    while (len(var) != 0):
        var.sort(reverse = True)
        del(buy[var[0]])
        del(var[0])
        
    # Makes a buy 
    if (threshold[i] < min_threshold and len(buy) < tot_buy):
        buy_routine(df['Price'][i], df['Date'][i])
        buy_count += 1
                         
    elif (threshold[i] > max_threshold):
        # Start selling only if buys are >= 8
        if (len(buy) >= start_sell): 
            # Start Sell  
            for k in range(len(buy)):
                min_buy = min(buy)
                min_buy_time = buy_time[buy.index(min(buy))]
                min_sell_target = min_buy + (min_buy * sell_percent)        
                
                if (buy[k] >= min_sell_target and df['Price'][i] >= min_sell_target):
                    print('Buy:{} \n Buy time:{} \t Sell:{} \n Sell time:{}'.format(min_buy, min_buy_time, df['Price'][i], df['Date'][i]))
                    sell_routine(df['Price'][i], df['Date'][i], min_buy)
                    del(buy_time[buy.index(min(buy))])
                    del(buy[buy.index(min(buy))])

    # Price is dropping fast. Sell max buy at min loss    
    if (len(buy) != 0 and df['Price'][i] < (min(buy) - min(buy) * price_drop_percent)):
        temp_max = max(buy)
        temp_var = buy.index(max(buy))
        sell_routine(df['Price'][i], df['Date'][i], buy[temp_var])
        additional_buy_routine(df['Price'][i], df['Date'][i], temp_var)
        buy_count += 1


print('Net profit: ${}'.format(sum(gain)))
print('Total buys: {},'.format(buy_count), 'Total sells: {},'.format(len(sell)), 'Stocks held: {}'.format(len(buy)))
