import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#plt.style.use('ggplot')

file = 'threshold_25%corrected.csv'

def read_csv(file):
    df = pd.read_csv(file, index_col=False)
    return df

df = read_csv(file)
df.columns = ['Date', 'Step', 'Price', 'Momentum']
fig, ax1 = plt.subplots()
ax1.plot(df['Step'], df['Price'], '-o', color = 'blue', label = 'GC=F')
ax1.set_xlabel('Time step')
ax1.set_ylabel('Stock price')

ax2 = ax1.twinx()

ax2.plot(df['Step'], df['Momentum'], '-o', color = 'red', label = 'Momentum')
ax2.set_ylabel('Momentum')

fig.tight_layout()
plt.legend()
plt.show()

