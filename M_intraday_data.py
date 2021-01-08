# Get 1 minute interval data for upto 7 days
import os
import glob
import requests
import arrow
import pickle
import datetime
import numpy as np
import bs4 as bs
import pandas as pd
import pandas_datareader as web

def get_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies') # SP500
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = str(row.findAll('td')[0])
        temp = [char for char in ticker if char.isupper()]
        temp1 = ''.join(temp)
        if (len(temp1) < 6):
            tickers.append(temp1)
    with open('sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    return tickers

def get_data(ticker, data_range, data_interval):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    body = data['chart']['result'][0]    
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('Asia/Tokyo').datetime.replace(tzinfo = None),
                       body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    dg = pd.DataFrame(body['timestamp'])    
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas
    df.drop(df.columns[[0, 1, 2, 4]], axis = 1, inplace = True)

    for i in range(0, len(df)):
        if (np.isnan(df.iloc[i]['CLOSE']) == True):
            df['CLOSE'][i] = (df['CLOSE'][i - 2] + df['CLOSE'][i - 1]) / 2
    return df

if __name__ == "__main__":
    tickers = get_tickers()
    if not os.path.exists('Intraday_stock_data'):
        os.makedirs('Intraday_stock_data')
        
    for ticker in tickers:
        print(ticker)
        data = get_data(ticker, '7d', '1m')
        data.to_csv('Intraday_stock_data/{}.csv'.format(ticker))
