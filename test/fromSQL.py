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
import pymysql
import sqlconfig # From sqlconfig.py
import sqlalchemy
import psycopg2




server = flask.Flask(__name__)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

Plot_wwidth = 600
Plot_hheight = 600
locations = pd.Series([" Wifi"," LTE"])

colors = {
    'background': '#303030', #black
    'DDbackground': '#d3d3d3', 
    'DDtext': '#d3d3d3', 
    'text': '#FFFFFF'  
}
'''
colors = {
    'background': '#FFFFFF', #white
    'text': '#000000'
}
'''

link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5JRPuanz8kRkVKU6BsZReBNENKglrLQDj1CTWnM1AqpxdWdWb3BEEzSeIcuPq9rSLNwzux_1l7mJb/pub?gid=1668794547&single=true&output=csv'

def tz_NYC(d): #timezone conversion
        d.index = d.index.tz_convert('America/New_York')
        return d

#observation =  pd.read_csv(link)
observation =  pd.read_csv(link, parse_dates=["Timestamp_Overrode"], index_col=["Timestamp_Overrode"])
observation.index = observation.index.tz_localize('America/New_York',ambiguous='infer')

notes= pd.DataFrame(observation[['note','sensor','Coord_X_m', 'Coord_Y_m', 'Coord_Z_m','Position_HumanReadable']])
notes.sort_index( inplace=True )
notes = notes["2019-09-05 ":"2019-12-10 "]

base_path = os.path.abspath(os.getcwd())
print(base_path)
values = pd.read_json(os.path.join(base_path,"values.json"))

query1= ''' 
SELECT * 
FROM cbasdef
WHERE sensor = 'BEEM-A' 
'''
query2= ''' 
SELECT * 
FROM cbasdef
WHERE sensor = 'BEEM-C' 
'''
query3= ''' 
SELECT * 
FROM cbasdef
WHERE sensor = 'BEEM-D' 
'''
query4= ''' 
SELECT * 
FROM cbasdef
WHERE sensor = 'Moe'
'''
query5= ''' 
SELECT * 
FROM cbasdef
WHERE sensor = 'protoCBAS-G' 
'''
path = [query1,query2,query3,query4,query5]

passwd = sqlconfig.passwd  # From sqlconfig.py
user = sqlconfig.user  # From sqlconfig.py
DB = 'cbas'  #name of databases to activate 

engine = sqlalchemy.create_engine('postgresql+psycopg2://'+user+':'+passwd+'@34.68.85.80/'+DB)

dfs =  [pd.read_sql(f,engine,index_col=["timestamp"])for f in path]



availablecolumns = pd.Series(dfs[0].columns).sort_values()

#cleanup traces 
#Apply any filtering needed before plotting
#[d.drop_duplicates(subset=['RCO2','Tdb_BME680'],keep = 'first', inplace = True) for d in dfs]  #remove duplicates for specific columns where sensor gets "stuck" 
#dfs[1]["2019-09-05 ":"2019-11-10 "]["RCO2"] = (dfs[1]["2019-09-05 ":"2019-11-10 "]["RCO2"]-782) #adjust for gremlins in CBAS-B CO2 sensor
#dfs =  [d.loc[d["Position_HumanReadable"] != '"Wind Tunnel"'] for d in dfs] # drop based on "Position_HumanReadable" column


#dfs = list(map(tz_NYC, dfs))

# plotting formatting
# this solves the axis presentation issues where you didn't know what day you were looking at when you zoomed in tight
ttickformatstops=[
    go.layout.xaxis.Tickformatstop(
        dtickrange=[None, 1000], value="%e-%b <br> %a <br> %H:%M:%S.%L"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[1000, 60000], value="%e-%b <br> %a <br> %H:%M:%S"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[60000, 3600000], value="%e-%b <br> %a <br> %H:%M"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[3600000, 86400000], value="%e-%b <br> %a <br> %H:%M"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[86400000, 604800000], value="%e-%b <br> %a"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[604800000, "M1"], value="%e-%b"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=["M1", "M12"], value="%b '%y"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=["M12", None], value="%Y Y")
]

llayoutFont = dict(
#    family = "Franklin Gothic Book, Arial")
    family = "Arial, Helvetica, Verdana, Franklin Gothic")

#set number of points that shows up on a plot. set to 0 for all of the points
mmaxDisplayed = 600

mmarker = dict(symbol = "circle-open",
            size = 3, 
            maxdisplayed = mmaxDisplayed)

smarker = dict(symbol = "hexagram-open",
            size = 3, 
            maxdisplayed = mmaxDisplayed)

nmarker = dict(symbol = "circle",
            size = 5)            


app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)

app.layout = html.Div([
  html.Div([
    dcc.Dropdown(
      id='yaxis-column_sol',
      options=[{'label': i, 'value': i} for i in availablecolumns],
      value='PPD'
      ),
    dcc.Dropdown(
      id='yaxis-column_df',
      options=[{'label': i, 'value': i} for i in availablecolumns],
      value='RCO2'
      ),
    dcc.Graph(
      id='Live-layout',
      #figure={'data': datatraced,'layout':layout}
    )
  ]),
])

@app.callback(Output('Live-layout', 'figure'),
              [Input('yaxis-column_df', 'value'),
               Input('yaxis-column_sol', 'value')])
def update_graph_live(value,y_value): 


    traceToPlot = dfs
    
    Valunit = list(values.unit.where(values.name == value).dropna())

    Valtitle = list(values.title.where(values.name == value).dropna())

    YValunit = list(values.unit.where(values.name == y_value).dropna())

    YValtitle = list(values.title.where(values.name == y_value).dropna())

    notes["Y"] = dfs[1][value].median()

    fig = go.Figure()

    [
    # Line Plot
    fig.add_trace(
        go.Scatter(x=d.index, y=d[y_value], name="Y"+d["sensor"].iloc[0],
        hoverinfo= "x+y+text",
        mode="markers+lines",marker = smarker,opacity=0.3))
    for d in traceToPlot
    ]
    #Notes Marker Plot
    fig.add_trace(
    go.Scatter(
        x=notes.index,
        y=notes['Y'],
        name='notes',
        mode="markers",
        marker = nmarker,
        hovertext=notes.note)) 
    fig.update_layout(
    title_text=Valtitle[0]+" (markers) & "+YValtitle[0] + " (lines)",
    autosize=False,
    width = Plot_wwidth,
    height = Plot_hheight,   
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            font=dict(family="Arial, Helvetica, Verdana", size=18)),
        type="date",
#       rangeslider=dict(visible=True),
        rangeslider=dict(visible=False),
        hoverformat="%a-%d %H:%M",
        #showspikes= False,
        #tickangle= 45,
        tickformatstops=ttickformatstops,
        ),

    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text=" (" + Valunit[0]+ " )",
            font=dict(size=12)))   

    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port = 8082)

