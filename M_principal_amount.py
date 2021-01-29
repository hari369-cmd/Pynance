import os
import sys
import csv
import math
import numpy as np
import pandas as pd
import tkinter as tk
from pathlib import Path


class Example(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="paleturquoise")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((55,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        
    def populate(self, tickers, stocks, price):
        tk.Label(self.frame, text="Stocks held", width=10, borderwidth="1",
                     relief="raised", bg="lawngreen").grid(row=0, column=0)
        tk.Label(self.frame, text="Ticker", width=10, borderwidth="1",
                     relief="raised", bg="lawngreen").grid(row=0, column=1)
        tk.Label(self.frame, text="Price/stock ($)", width=20, borderwidth="1",
                     relief="raised", bg="lawngreen").grid(row=0, column=2)
        for row, ticker in enumerate(tickers):
            if (stocks[row] != 0):
                col = "white"
            else:
                col = "lavender"
                
            tk.Label(self.frame, text=stocks[row], width=10, borderwidth="1",
                     relief="solid", bg=col).grid(row=row+1, column=0) 
            tk.Label(self.frame, text=ticker, width=10,
                     relief="raised", bg=col).grid(row=row+1, column=1)
            tk.Label(self.frame, text=price[row], width=20,
                     relief="raised", bg=col).grid(row=row+1, column=2)
            

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



def read_csv(file):
    df = pd.read_csv(file, index_col = False)
    return df

def write_csv(data, file):
    with open(file, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


def ind_principal_amount_calc(p_amount_stocks, P_amount, ind_tot_buys, rank):
    temp_tot_amount = 0.0
    tot_amount = 0.0
    end_flag = 0
    loop = 0
    
    while (end_flag == 0):
        loop += 1
        for i in range(0, len(p_amount_stocks), 1):
            if (rank[i] == 0):
                temp_tot_amount += p_amount_stocks[i]
                if (temp_tot_amount <= P_amount):
                    ind_tot_buys[i] += 1
                else:
                    diff = temp_tot_amount - P_amount
                    if (diff < min(p_amount_stocks) and loop == 1):
                        tot_amount = temp_tot_amount - p_amount_stocks[i]
                        end_flag = 1
                    elif (diff < min(p_amount_stocks) and loop > 1):
                        tot_amount = temp_tot_amount - p_amount_stocks[i]
                        end_flag = 1
                    elif (diff > min(p_amount_stocks) and diff < p_amount_stocks[i]):
                        temp_tot_amount -= p_amount_stocks[i] 
                        continue
    return (tot_amount, ind_tot_buys)



def calc_weights(ind_tot_buys):
    weights = []
    sum_ = sum(ind_tot_buys)
    if (sum_ == 0):
        sum_ = 1
    for i in range(0, len(ind_tot_buys), 1):
        weights.append(ind_tot_buys[i] / sum_)
    return (weights)


def data_table(tickers, ind_tot_buys, price):
    root=tk.Tk()
    root.geometry("500x1000")
    example = Example(root)
    example.populate(tickers, ind_tot_buys, price)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()


def pre_trading_principal():
    path = Path(os.getcwd() + '/Intraday_stock_data')
    tickers = [file.stem for file in path.iterdir() if file.suffix == '.csv']
    if (len(tickers) == 0):
        sys.exit('CSV stock files not found in {}'.format(path))  
    num_stocks = len(tickers)
    p_amount_calc = 0
    p_amount_stocks = []

    for ticker in tickers:
        df = read_csv('Intraday_stock_data/{}.csv'.format(ticker))
        df.columns = ['Date', 'Price']
        p_amount_stocks.append(df['Price'][29])
        p_amount_calc += df['Price'][29]
    
    print('Ideal initial investment: $ {}'.format(sum(p_amount_stocks)))
    while True:
        try:
            P_amount = float(input('Enter principal trading amount in USD: '))
            loc_var = P_amount / 100
            break
        except:
            print('Enter a valid amount.')
            
    # Assigning default equal weights to all stocks
    ind_tot_buys = np.zeros(len(p_amount_stocks))
    rank = np.zeros(len(p_amount_stocks))
    tot_amount, int_tot_buys = ind_principal_amount_calc(p_amount_stocks, P_amount, ind_tot_buys, rank)
    print(tot_amount, P_amount)
    weights = calc_weights(ind_tot_buys)

    # If we wish to change the weights stocks
    change = input('Type y to change the number of stocks held or n to continue with default stock arrangement: ')
    while (change == 'y'):
        # If we wish to change the weights for multiple stocks
        option = input('Type m for multiple stock correction or s for single stock correction: ')
        if (option == "m"):
            data_table(tickers, ind_tot_buys, p_amount_stocks)
            txt = input('Input tickers and stocks: ')
            loc_var = txt.split(',')
            ticker_input = []
            tot_buy_input = []
            temp_sum = 0
            temp_tot = 0
            for i in range(len(loc_var)):
                loc_var1 = loc_var[i].split()
                ticker_input.append(loc_var1[0])
                tot_buy_input.append(int(loc_var1[1]))
            for i in range(len(tot_buy_input)):
                temp_sum += (tot_buy_input[i] * p_amount_stocks[tickers.index(ticker_input[i])])
                
            temp_tot = P_amount - temp_sum
            if (temp_tot < 0):
                print('Error: Entry(ies) too large')
                continue
            else:
                ind_tot_buys[:] = 0
                for i in range(len(tot_buy_input)):
                    ind_tot_buys[tickers.index(ticker_input[i])] = tot_buy_input[i]
                    rank[tickers.index(ticker_input[i])] = 1
                tot_amount, ind_tot_buys = ind_principal_amount_calc(p_amount_stocks, temp_tot, ind_tot_buys, rank)
                tot_amount += temp_sum
                weights = calc_weights(ind_tot_buys)    
                print(sum(weights), tot_amount)
                rank[:] = 0
                data_table(tickers, ind_tot_buys, p_amount_stocks)
            change = input('Type y to change the number of stocks held or n to continue with default stock arrangement: ')

        # If we wish to change the weights for a given stock
        else:
            data_table(tickers, ind_tot_buys, p_amount_stocks)
            while True:
                try:
                    ticker_input = input('Enter the ticker name for changing the number of stocks: ')
                    loc_var = tickers[tickers.index(ticker_input)]
                    break
                except:
                    print('{} is not a valid ticker.'.format(ticker_input))
                    data_table(tickers, ind_tot_buys, p_amount_stocks)
                
            print('{} has {} stocks'.format(ticker_input,
                                            ind_tot_buys[tickers.index(ticker_input)]))
            while True:
                try:
                    tot_buy_input = int(input('Enter the new number: '))
                    break
                except:
                    print('Please enter an integer value')
                
            temp_tot = (P_amount - (tot_buy_input * p_amount_stocks[tickers.index(ticker_input)]))
            if (temp_tot < 0):
                print('Error: Entry too large')
                continue
            else:
                ind_tot_buys[:] = 0
                ind_tot_buys[tickers.index(ticker_input)] = tot_buy_input
                rank[tickers.index(ticker_input)] = 1
                tot_amount, ind_tot_buys = ind_principal_amount_calc(p_amount_stocks, temp_tot, ind_tot_buys, rank)
                tot_amount += (tot_buy_input * p_amount_stocks[tickers.index(ticker_input)])
                weights = calc_weights(ind_tot_buys)    
                print(sum(weights), tot_amount)
                rank[:] = 0
                data_table(tickers, ind_tot_buys, p_amount_stocks)
            change = input('Type y to change the number of stocks held or n to continue with the current allocation: ')
        
    return (tickers, ind_tot_buys)


if __name__=="__main__":
    tickers, stocks = pre_trading_principal()
