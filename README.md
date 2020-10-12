# Pynance

# Instructions on how to run the code

The requirements.txt file contains the necessary Python packages with the versions you need to run the script.
Just run $pip install -r requirements.txt to first install everything necessary.

Since the Selenium part is not included yet, the code can be operated (for now) only in the pre-existing data mode (_LIVE_ = 0).
If you do not have any pre-existing stock data, do the following:
1. Set _get_data_ = 1 and make sure _LIVE_ = 0
2. Change the 'GC=F' in the _ticker_ variable for a ticker of your choice
3. Set the _start_ and _end_ times during which the data is required. The data will be obtained from Yahoo finance and the default data interval is 1 day. 
4. Run the code.

Running the code will save a csv file titled "xx.csv", where xx is the ticker, to the local folder your code is in.

# What to expect from the code

The code will calculate a parameter called "_threshold_" and this parameter will lie in the range [-1, 1]. The _threshold_ is calculated as an average of momentum deciding parameters obtained from 7 technical indicators. The 7 indicators are as follows:
1. Moving Average (ma)
2. Exponential Moving Average (ema)
3. Moving Average Convergence Divergence (macd)
4. Bollinger Bands (bb)
5. Relative Strength Index (rsi)
6. Commodity Channel Index (cci)
7. Stochastic Oscillator (si)

The momentum deciding parameters obtained from these 7 indicators also lie in the range [-1, 1]. The momentum deciding parameters are estimated based on the difference between the current and average of previous prices parameter called "_diff_" and based on variables corresponding to each indicator.

The _diff_ parameter is decided by comparing with a parameter called "_min_per_change_". _min_per_change_ is the minimum percentage of change required between current price of the stock and the average of previous prices and is set by the user. _min_per_change_ is positive if _diff_ is positive and so on. Thus _min_per_change_ acts as the sensitivity parameter. Fine tuning can be done by adjusting the weights and variables in each technical indicator.
