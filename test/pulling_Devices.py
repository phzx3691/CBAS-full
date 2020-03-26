import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as FF
import plotly.offline as offline
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import os.path
from datetime import datetime
from dash.dependencies import Input, Output
import glob
import flask
from tqdm import tqdm
from scipy.constants import convert_temperature
import sqlconfig # From sqlconfig.py
import sqlalchemy
import psycopg2
print("Import Complete")


passwd = sqlconfig.passwd  # From sqlconfig.py
user = sqlconfig.user  # From sqlconfig.py
DB = 'cbas'  #name of databases to activate 

engine = sqlalchemy.create_engine('postgresql+psycopg2://'+user+':'+passwd+'@34.68.85.80/'+DB)




query = '''
SELECT * 
FROM raw
-- WHERE timestamp > NOW() - interval '1 hour';
'''

df = pd.read_sql(query,engine,index_col=["timestamp"])

sensors = df.sensor.unique()

dfs = {}
for s in sensors:
    dfs[s] = df.where(df["sensor"] == s).dropna()

# for Ipyn
'''
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
for key in dfs.values(): 
    display(key.head())
'''
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def Printthis(dataframes):
    for key in dataframes.values(): 
        display(key.head())

Printthis(dfs)

mmarker = dict(symbol = "circle-open",
            size = 5, 
            maxdisplayed = 300)



fig = go.Figure([go.Scatter(x=key.index, y=key['Tdb_BME680'], name=key["sensor"].iloc[0],
    hoverinfo= "x+y+text+name",mode="markers+lines",marker = mmarker) for key in dfs.values()])

fig.show()


# old function convert 

for d in dfs.values():
    d["Tdb_BME680F"] = convert_temperature(d["Tdb_BME680"].dropna(), 'Celsius', 'F')
    d["Tdb_BME680F"][d["Tdb_BME680F"] < 50] = np.NaN



fig = go.Figure([go.Scatter(x=key.index, y=key['Tdb_BME680F'], name=key["sensor"].iloc[0],
    hoverinfo= "x+y+text+name",mode="markers+lines",marker = mmarker) for key in dfs.values()])

fig.show()
