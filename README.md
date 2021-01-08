Files in this folder:
01) M_buy_sell_routine.py
02) M_intraday_data.py
03) test_diff.py
04) test_threshold.py

Files starting with 'M' can be imported as modules or can be compiled individually.

Instructions:
01) Run M_intraday_data.py as an individual code.
02) Run test_diff.py
03) Run test_threshold.py

What the code does:
01) M_intraday_data.py
When executed as an individual file, it creates a folder 'Intraday_stock_data'. Then 1 week intraday data (1 min intervals) is obtained from Yahoo finance for 136 companies and is saved in the 'Intraday_stock_data' folder as csv files.
When executed as a module, it is usually imported as 'mid' in test_diff.py and test_threshold.py and is primarily used to obtain the tickers of the 136 companies.

02) test_diff.py
When executed, it creates a folder 'stocks_diff'. It reads through the csv files in the 'Intraday_stock_data' folder and finds the diff parameter along with the mean, variance and standard deviation for the stock prices. It then outputs a csv file ({company}_diff.csv) in the 'stocks_diff' folder. These output files are then re-read in the second half of execution and the profits are estimated using the M_buy_sell_routine.py module imported as bsr. The    profits of each company is combined into a single csv file and is exported as 'profits_diff.csv'.

03) test_threshold.py
Similar to test_diff.py, when executed, it creates a folder 'stocks_threshold'. It reads through the csv files in the 'Intraday_stock_data' folder and finds the threshold parameter along with the mean, variance and standard deviation for the stock prices. It then outputs a csv file ({company}_threshold.csv) in the 'stocks_threshold' folder. These output files are then re-read in the second half of execution and the profits are estimated using the M_buy_sell_routine.py module imported as bsr. The profits of each company is combined into a single csv file and is exported as 'profits_threshold.csv'.