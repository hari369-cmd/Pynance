import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_csv(file):
    df = pd.read_csv(file, index_col = False)
    return df

def write_csv(data, file):
    with open(file, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

def load_bsr(ticker, file, method):
    print('Ticker: {}'.format(ticker))
    df = read_csv(file)    
    df.columns = ['Date', 'Price', 'Threshold', 'Variance', 'Std Dev']
    temp = range(0, len(df['Date']), 1)
    threshold = df['Threshold']
    variance = df['Variance']
    std_dev = df['Std Dev']
    
    tot_buy = 6
    buy = []
    buy_time = []
    sell = []
    sell_time = []
    gain = []
    var = []
    loss_stocks = []
    loss_amount = []

    #min_threshold = -0.2 #-0.2 #0.0005
    #max_threshold = 0.2 #0.2 # -0.0015 
    price_drop_percent = 1.2
    transaction_cost = 0.03
    buy_count = 0
    principal_amount = 1.0
    latest_buy_price = 0.0
    latest_buy_threshold = 0.0 

    def buy_routine(price, time):
        buy.append(price)
        buy_time.append(time)
        nonlocal principal_amount
        principal_amount += price

    def additional_buy_routine(price, time, index):
        buy[index] = price
        buy_time[index] = time
        nonlocal principal_amount
        principal_amount += price
    
    def sell_routine(price, time, min_buy):
        sell.append(price)
        gain.append(price - min_buy)
        sell_time.append(time)

    if method == 'diff':
        var1 = 1
        var2 = -1
    else:
        var1 = -1
        var2 = 1
        
    for i in range(0, len(df['Price'])):

        min_threshold = var1 * variance[i]
        max_threshold = var2 * variance[i]
        
        temp_sell_last_order = 0
        for k in range(0, len(buy)):
            temp_sell_last_order += (df['Price'][i] - buy[k])

        if (tot_buy == 0 or (sum(gain) + temp_sell_last_order) < 0):
            print('Trading completed at {} out of {}'.format(i, len(df['Price'])))
            break

        # Selling any buys with sufficient profits
        for j in range(0, len(buy)):
            profitable_target = buy[j] + (buy[j] * 4 * transaction_cost)
            if (df['Price'][i] >= profitable_target):
                sell_routine(df['Price'][i], df['Date'][i], buy[j])
                var.append(j)
        # Remove buys that were sold
        while (len(var) != 0):
            var.sort(reverse = True)
            del(buy[var[0]])
            del(var[0])

        # Price is dropping fast. Sell max buy at min loss    
        if (len(buy) != 0 and df['Price'][i] < (max(buy) - max(buy) * price_drop_percent)):
            temp_max = max(buy)
            temp_var = buy.index(max(buy))
            sell_routine(df['Price'][i], df['Date'][i], buy[temp_var])
            additional_buy_routine(df['Price'][i], df['Date'][i], temp_var)
            buy_count += 1
        
        if (threshold[i] > min_threshold and len(buy) < tot_buy):
            if (latest_buy_price != df['Price'][i] and latest_buy_threshold != threshold[i]):
                latest_buy_price = df['Price'][i]
                latest_buy_threshold = threshold[i]
                buy_routine(df['Price'][i], df['Date'][i])
                buy_count += 1
                         
        elif (threshold[i] < max_threshold and len(buy) != 0):
            min_buy = min(buy)
            min_buy_time = buy_time[buy.index(min(buy))]
            min_target = min_buy + (min_buy * 2 * transaction_cost)        
            if (df['Price'][i] >= min_target):
                sell_routine(df['Price'][i], df['Date'][i], min_buy)
                del(buy_time[buy.index(min(buy))])
                del(buy[buy.index(min(buy))])

        # Decrease the number of stocks held for every given number of sells
        if (len(sell) % 2 == 0 and len(sell) != 0 and len(buy) != 0):
            tot_buy = tot_buy - 1
            
        # Decrease the number of stocks held for every given number of time steps
        if (i % 500 == 0 and len(sell) < (int(i / 1000)) and len(buy) != 0):
            loc_temp = 0
            loc_temp_index = 0
            for j in range(0, len(buy)):
                temp_diff = df['Price'][i] - buy[j]
                if (temp_diff > loc_temp):
                    loc_temp = temp_diff
                    loc_temp_index = j
            
            sell_routine(df['Price'][i], df['Date'][i], buy[loc_temp_index])
            del(buy_time[loc_temp_index])
            del(buy[loc_temp_index])
            tot_buy = tot_buy - 1

    
    # Sell all the buys being held as the last order
    sell_last_order = 0
    for k in range(0, len(buy)):
        sell_last_order += (df['Price'][len(df['Price']) - 1] - buy[k])
    buy = []

    write_csv([ticker, (sum(gain) + sell_last_order), principal_amount,
               (sum(gain) + sell_last_order)/principal_amount], 'profits_{}.csv'.format(method))
    print('Total buys: {},'.format(buy_count), 'Total sells: {},'.format(len(sell)),
          'Stocks held: {}'.format(len(buy)))
    print('Net profit: ${}'.format((sum(gain) + sell_last_order)))
    print('Pricipal amount: ${}'.format(principal_amount))
