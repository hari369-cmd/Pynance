import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#plt.style.use('ggplot')

file = 'threshold.csv'

def read_csv(file):
    df = pd.read_csv(file, index_col=False)
    return df

indicators = ['Stock price', 'MA', 'EMA', 'MACD', 'BB', 'RSI', 'CCI', 'SO']

len1 = 2
len2 = 2
df = read_csv(file)
df.columns = ['Date', 'Price', 'MA', 'EMA', 'MACD', 'BB', 'RSI', 'CCI', 'SO', 'Threshold']
temp = range(0, len(df['Date']), 1)
threshold = df['Threshold']

buy = []
buy_time = []
sell = []
sell_time = []
temp = []
temp1 = []
gain = []

for i in range(0, len(df['Price'])):
    if (threshold[i] < -0.2):
        buy.append(df['Price'][i])
        buy_time.append(df['Date'][i])
                
    if (threshold[i] > 0.3):
        if (len(buy) == 0):
            continue
        else:
            for j in range(0, len(buy)):
                if (df['Price'][i] > buy[j]):
                    print('Buy:{}'.format(buy[j]), 'Sell:{}'.format(df['Price'][i]))
                    temp.append(buy[j])
                    temp1.append(buy_time[j])
                    sell.append(df['Price'][i])
                    gain.append(df['Price'][i] - buy[j])
                    sell_time.append(df['Date'][i])
            buy.clear()

print(sum(gain))
print('buy:{} {}'.format(temp, temp1))
print('sell:{} {}'.format(sell,sell_time))
    
