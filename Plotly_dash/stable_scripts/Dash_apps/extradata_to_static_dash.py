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

server = flask.Flask(__name__)

Plot_wwidth = 700
Plot_hheight = 400
locations = pd.Series([" Wifi (BEEM)"," LTE (roaming)"])

colors = {
    'background': '#303030', #black
    'DDbackground': '#d3d3d3', #
    'DDtext': '#d3d3d3', 
    'text': '#FFFFFF'  
}
'''
colors = {
    'background': '#FFFFFF', #white
    'text': '#000000'
}
'''


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']


link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5JRPuanz8kRkVKU6BsZReBNENKglrLQDj1CTWnM1AqpxdWdWb3BEEzSeIcuPq9rSLNwzux_1l7mJb/pub?gid=1668794547&single=true&output=csv'


#observation =  pd.read_csv(link)
observation =  pd.read_csv(link, parse_dates=["Timestamp_Overrode"], index_col=["Timestamp_Overrode"])
observation.index = observation.index.tz_localize('America/New_York',ambiguous='infer')

notes= pd.DataFrame(observation[['note','sensor','Coord_X_m', 'Coord_Y_m', 'Coord_Z_m','Position_HumanReadable']])
notes.sort_index( inplace=True )
notes = notes["2019-09-05 ":"2019-12-10 "]

#scan script for "filePathUpdate" to swap out local file paths per your machine - NN

#set paths
samprt_path = ""'5T'""
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
start_path = os.path.join(base_path, "CSV", "2Interim","4_generateComfortMetrics")
fn = 'protoCBAS-*'
path = sorted(glob.glob(os.path.join(start_path, fn)))
values = pd.read_json(os.path.join(base_path,"values.json"))

dfs = [pd.read_csv(f, parse_dates=["timestamp"], index_col=["timestamp"]).assign(sensor=f) for f in path]
availablecolumns = pd.Series(dfs[0].columns).sort_values()
## filtering directory/file extensions
stripboard = ((len(start_path))) # getting the length of the path up to where glob fills in filenames

for d in dfs:
    d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")


def tz_NYC(d): 
        d.index = d.index.tz_convert('America/New_York')
        return d

dfs = list(map(tz_NYC, dfs))
#availablecolumns.drop('timestamp')


#cleanup traces 
#Apply any filtering needed before plotting
#[d.drop_duplicates(subset=['RCO2','Tdb_BME680'],keep = 'first', inplace = True) for d in dfs]  #remove duplicates for specific columns where sensor gets "stuck" 
dfs[1]["2019-09-05 ":"2019-11-10 "]["RCO2"] = (dfs[1]["2019-09-05 ":"2019-11-10 "]["RCO2"]-782) #adjust for gremlins in CBAS-B CO2 sensor
dfs = [d.loc[d["Position_HumanReadable"] != '"Wind Tunnel"'] for d in dfs] # drop based on "Position_HumanReadable" column


#wtdfs = [d["2019-09-21 ":"2019-10-10 "] for d in dfs]


#Index(['timestamp', 'Air', 'Alt_BME680', 'ECO2', 'Lux', 
# 'PM1', 'PM10', 'PM25','P_BME680', 'RCO2', 'RH_BME680', 
# 'RH_scd30', 'TVOC', 'Tdb_BME680','Tdb_scd30', 'battery', 'epoch'],dtype='object')


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



app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)

app.layout = html.Div([
  html.Div([
    dcc.Dropdown(
      id='yaxis-column',
      options=[{'label': i, 'value': i} for i in availablecolumns],
      value='Air',
      style={'backgroundColor': colors['DDbackground'],'color': colors['text'],'box-shadow': '0px 8px 16px 0px rgba(0,0,0,0.2)' }

      ),
    dcc.Graph(
      id='Live-layout',
      #figure={'data': datatraced,'layout':layout}
    )
  ]),
])

@app.callback(Output('Live-layout', 'figure'),
              [Input('yaxis-column', 'value')])
def update_graph_live(value): 

    traceToPlot = dfs
    
    Valunit = list(values.unit.where(values.name == value).dropna())

    Valtitle = list(values.title.where(values.name == value).dropna())

    notes["Y"] = dfs[1][value].median()

    fig = go.Figure()

    [
    fig.add_trace(
        go.Scatter(x=d.index, y=d[value], name=d["sensor"].iloc[0],
        hovertext=d.Position_HumanReadable,hoverinfo= "x+y+text+name",
        mode="markers",marker = mmarker))
    for d in traceToPlot
    ]
    fig.add_trace(
    go.Scatter(
        x=notes.index,
        y=notes['Y'],
        name='notes',
        mode="markers",
        hovertext=notes.note))
    fig.update_layout(
    title_text=Valtitle[0],
    autosize=False,
    width = Plot_wwidth,
    height = Plot_hheight,
    font = {'color': colors['text'] },
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],        
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            font=dict(family="Arial, Helvetica, Verdana", size=18)),
        type="date",
#        rangeslider=dict(visible=True),
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
