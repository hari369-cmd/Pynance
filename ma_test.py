import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from activation_threshold import moving_average 
from window_slider import Slider
import numpy

df = pd.read_csv('/Users/ks/bot/Pynance/data/GC=F.csv', index_col=False)
df.columns = ['Time','Price']
# to make a batch of 60 i.e. 60*24=1440
df_test = df.append(df.tail(2))
time_steps = 60 # Minimum number of time data required
c = time_steps - 1

def diff_calc(data_f):
    df_temp = data_f
    loc_avg = sum(df_temp) / len(df_temp) 
    diff = (df_temp.iloc[c] - loc_avg) / df_temp.iloc[c]    
    return diff

diff_ = []

#Slider for df with bucket size = 60
bucket_size = time_steps 
#Slider movement up by 1 i.e. overlaps of 59
overlap_count = c
slider = Slider(bucket_size,overlap_count)
slider.fit(df_test['Price'])       
while True:
    window_data = slider.slide()
    if len(window_data) == 60:
        diff = diff_calc(window_data)
        diff_.append(diff)
    else:
        diff_.append(None)
    if slider.reached_end_of_list(): 
        break


# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df_test['Time'], y=df_test['Price'], name="Gold Price"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df_test['Time'], y=diff_, name="MA_Diff"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Price vs MA Indicator (Diff)"
)

# Set x-axis title
fig.update_xaxes(title_text="Time(in minutes)")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Gold Prices</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>MA_Diff</b>", secondary_y=True)

fig.show()



