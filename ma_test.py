import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from activation_threshold import moving_average 
from window_slider import Slider
import numpy
import M_intraday_data as mi
import argparse
import plotly.express as px


parser = argparse.ArgumentParser(description="Visualize indicators and price chart")
parser.add_argument('-l','--location', type=str, required=True, help='Location of the stock data in csv')
args = parser.parse_args()

time_steps = 60 
c = time_steps - 1

def pre_processing(location): 

    df = pd.read_csv(location, index_col=False)
    df.columns = ['Time','Close']
    if len(df) % 60 != 0:
        df_test = df.append(df.tail(len(df) % 60))
    else:
        df_test = df
    return df_test

def diff_logic(data_frame):

    loc_avg = sum(data_frame) / len(data_frame) 
    diff = (data_frame.iloc[c] - loc_avg) / loc_avg #or can use "df_test.iloc[c]" --> doesnt affect the plot
    return diff

def diff_calc(location):

    df_test = pre_processing(location)
    diff_ = []
    #Slider for df with bucket size = 60
    #Slider movement up by 1 i.e. overlaps of 59
    slider = Slider(time_steps,c)
    slider.fit(df_test['Close'])       
    while True:
        window_data = slider.slide()
        if len(window_data) == 60:
            diff = diff_logic(window_data)
            diff_.append(diff)
        else:
            diff_.append(None)
        if slider.reached_end_of_list(): 
            break
    
    if len(df_test) != len(diff_):
        diff_.extend([None]*(len(df_test)-len(diff_)))
        df_test['ma_diff'] = diff_
    
    return df_test

    
def plot_everything(location): 

    df_test = diff_calc(location)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df_test['Time'], y=df_test['Close'], name="Stock Price"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_test['Time'], y=df_test['ma_diff'], name="MA_Diff"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Price vs MA Indicator (Diff)"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time(in minutes)")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Stock Prices</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>MA_Diff</b>", secondary_y=True)

    fig.show()

def plot_stockonly(location):
    df_test = pre_processing(location)
    fig = px.line(df_test, x="Time", y="Close")
    fig.show()

def main():
    plot_everything(args.location)
    plot_stockonly(args.location)

if __name__=="__main__":
    main()