#This is a test script to get historical data with API
from alpha_vantage.timeseries import TimeSeries

API_KEY = '0PTXJ4PZJ0U0EF5Z'
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='APPL',interval='1min', outputsize='full')