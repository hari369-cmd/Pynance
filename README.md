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
1. Set $get_data$ = 1 and make sure $LIVE$ = 0
2. Change the 'GC=F' in the $ticker$ variable for a ticker of your choice
3. Set the $start$ and $end$ times during which the data is required. The data will be obtained from Yahoo finance and the default data interval is 1 day. 
4. Run the code.

Running the code will save a csv file titled "xx.csv", where xx is the ticker, to the local folder your code is in.

# What to expect from the code

The code will calculate a paramter called "$threshold$" and this parameter will lie in the range [-1, 1]. The $threshold$ is calculated as an average of momentum deciding parameters obtained from 7 technical indicators. The 7 indicators are as follows:
1. Moving Average (ma)
2. Exponential Moving Average (ema)
3. Moving Average Convergence Divergence (macd)
4. Bollinger Bands (bb)
5. Relative Strength Index (rsi)
6. Commodity Channel Index (cci)
7. Stochastic Oscillator (si)

The momentum deciding parameters obtained from these 7 indicators also lie in the range [-1, 1]. The momentum deciding parameters are estimated based on the difference between the current and average of previous prices parameter called "$diff$" and based on variables corresponding to each indicator.

The $diff$ parameter is decided by comparing with a parameter called "$min_per_change$". $min_per_change$ is the minimum percentage of change required between current price of the stock and the average of previous prices and is set by the user. $min_per_change$ is positive if $diff$ is positive and so on. Thus $min_per_change$ acts as the sensitivity parameter. Fine tuning can be done by adjusting the weights and variables in each technical indicator.
