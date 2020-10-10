# Pynance

# Instructions on how to run the code

Make sure you got the following libraries:

01) Beautiful soup
02) Pickle
03) Requests
04) datetime
05) csv
06) matplotlib
07) pandas
08) numpy

Since the Selenium part is not included yet, the code can be operated (for now) only in the pre-existing data mode (LIVE = 0).
If you do not have any pre-existing stock data, do the following:
1. Set get_data = 1 and make sure LIVE = 0
2. Change the 'GC=F' in the ticker variable for a ticker of your choice
3. Set the start and end times during which the data is required. The data will be obtained from Yahoo finance and the default data interval is 1 day. 
