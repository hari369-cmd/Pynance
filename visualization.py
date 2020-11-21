import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#plt.style.use('ggplot')

file = 'data_5_nov.csv'

def read_csv(file):
    df = pd.read_csv(file, index_col=False)
    return df

indicators = ['Stock price', 'MA', 'EMA', 'MACD', 'BB', 'RSI', 'CCI', 'SO']

len1 = 2
len2 = 4
df = read_csv(file)
df.columns = ['Date', 'Price', 'MA', 'EMA', 'MACD', 'BB', 'RSI', 'CCI', 'SO', 'Threshold']
fig, (ax1, ax2) = plt.subplots(len1, len2)
temp = range(0, len(df['Date']), 1)

ax1_twin = ax1[0].twinx()
ax1[0].plot(temp, df['Price'], '-', color = 'blue', label = 'GC=F')
ax1_twin.plot(temp, df['MA'], 'o', color = 'red', label = 'MA')
ax1[1].plot(temp, df['MA'], '-', color = 'red', label = 'MA')
ax1[2].plot(temp, df['EMA'], '-', color = 'green', label = 'EMA')
ax2[0].plot(temp, df['MACD'], '-', color = 'orange', label = 'MACD')
ax2[1].plot(temp, df['BB'], '-', color = 'violet', label = 'BB')
ax2[2].plot(temp, df['RSI'], '-', color = 'purple', label = 'RSI')
ax2[2].plot(temp, df['CCI'], '-', color = 'yellow', label = 'CCI')
ax2[3].plot(temp, df['SO'], '-', color = 'black', label = 'MA')
#plt.subplot(241)
#ax2[1].plot(temp, df['Threshold'], '-', color = 'teal', label = 'Threshold')
ax2[1].set_ylabel('Momentum')

for i in range(0, len(ax1)):
    ax1[i].set_xlabel('Time step')
    ax1[i].set_ylabel('{}'.format(indicators[i]))

for j in range(0, len(ax2)):
    ax2[j].set_xlabel('Time step')
    ax2[j].set_ylabel('{}'.format(indicators[j+len(ax1)]))

fig.tight_layout()
plt.legend()
plt.show()

