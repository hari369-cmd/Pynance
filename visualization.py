import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv('/Users/ks/bot/Pynance/data/data_5_nov.csv')

fig = make_subplots(rows=2, cols=2,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]])

# # Top left
# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
#     row=1, col=1, secondary_y=False)

# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['Threshold'], name="Threshold"),
#     row=1, col=1, secondary_y=True,
# )

# # Top right
# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
#     row=1, col=2, secondary_y=False,
# )

# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['SO'], name="SO"),
#     row=1, col=2, secondary_y=True,
# )

# # 2nd left
# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
#     row=2, col=1, secondary_y=False,
# )

# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['CCI'], name="CCI"),
#     row=2, col=1, secondary_y=True,
# )

# # 2nd right
# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
#     row=2, col=2, secondary_y=False,
# )

# fig.add_trace(
#     go.Scatter(x=df['Time'], y=df['RSI'], name="RSI"),
#     row=2, col=2, secondary_y=True,
# )

# 3rd left
fig.add_trace(
    go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
    row=1, col=1, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['Time'], y=df['BB'], name="BB"),
    row=1, col=1, secondary_y=True,
)

# 3rd right
fig.add_trace(
    go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
    row=1, col=2, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['Time'], y=df['MACD'], name="MACD"),
    row=1, col=2, secondary_y=True,
)

# Bottom left
fig.add_trace(
    go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
    row=2, col=1, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['Time'], y=df['EMA'], name="EMA"),
    row=2, col=1, secondary_y=True,
)

# Bottom right
fig.add_trace(
    go.Scatter(x=df['Time'], y=df['Price'], name="Price"),
    row=2, col=2, secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['Time'], y=df['MA'], name="MA"),
    row=2, col=2, secondary_y=True,
)


fig.show()

