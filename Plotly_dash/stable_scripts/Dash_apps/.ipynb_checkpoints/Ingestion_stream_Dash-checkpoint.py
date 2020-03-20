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

server = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#start_path = '/home/sheldon/ingest/sensor-feed/csv/'


Plot_wwidth = 700
Plot_hheight = 400
locations = pd.Series([" Wifi (Moe)"," LTE (roaming)"])

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


link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5JRPuanz8kRkVKU6BsZReBNENKglrLQDj1CTWnM1AqpxdWdWb3BEEzSeIcuPq9rSLNwzux_1l7mJb/pub?gid=1668794547&single=true&output=csv'

def tz_NYC(d): #timezone conversion
        d.index = d.index.tz_convert('America/New_York')
        return d

observation =  pd.read_csv(link, parse_dates=["Timestamp_Overrode"], index_col=["Timestamp_Overrode"])
observation.index = observation.index.tz_localize('America/New_York',ambiguous='infer')

notes= pd.DataFrame(observation[['note','sensor','Coord_X_m', 'Coord_Y_m', 'Coord_Z_m','Position_HumanReadable']])
notes.sort_index( inplace=True )
notes = notes["2020-01-01 ":"2020- "]

#set paths
samprt_path = ""'5T'""
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(" Base Path: " + base_path)
home_path = os.path.dirname(os.path.dirname(base_path))
ingest_path = os.path.join(base_path,"CSV","3Raw","From_Ingestions","ingestions_BK")
#ingest_path = os.path.join(base_path,"CSV","2Interim","4_generateComfortMetrics")

print(" ingest Path: " + ingest_path)
#fn = 'protoCBAS-*'
fn = 'cbas_IN-*'   # CSVs from ingestion start
path = sorted(glob.glob(os.path.join(ingest_path, fn)))
print(" Paths: " + str(path))
values = pd.read_json(os.path.join(base_path,"values.json"))

dfs = [pd.read_csv(f, parse_dates=["timestamp"], index_col=["timestamp"]).assign(sensor=f) for f in tqdm(path,desc="Reading CSVs...")]
for d in dfs:
    d["Tdb_BME680F"] = convert_temperature(d["Tdb_BME680"].dropna(), 'Celsius', 'F')
    d["Tdb_BME680F"][d["Tdb_BME680F"] < 50] = np.NaN
availablecolumns = pd.Series(dfs[0].columns).sort_values()



filterCriteria_0th = [("battery", 2, "less"), ("RCO2", 0, "less"),
                      ("RCO2", 5000, "greater"), ("Tdb_BME680", 0, "less"),
                      ("Tdb_scd30", 0, "less"), ("Tdb_scd30", 101, "greater"),
                      ("PM25", 5000, "greater"), ("PM25", 0, "less"),
                      ("Lux", 100000, "greater"), ("RH_scd30", 0, "less"),
                      ("RH_scd30", 101, "greater"), ("RH_BME680", 0, "less"),
                      ("RH_BME680", 101, "greater"), ("Air", 20, "greater"),
                      ("TVOC", 0, "less"),("Lux", 0, "less"),("P_BME680", 0, "less"),
                      ("Alt_BME680", 0, "less")]


def setNaN(dataframes, key, value, comparetype="less"):
       for d in dataframes:
           if comparetype == "less":
               d[key][d[key] < value] = np.NaN
           elif comparetype == "greater":
               d[key][d[key] > value] = np.NaN
           else:
               d[key][d[key] == value] = np.NaN



## filtering directory/file extensions
stripboard = ((len(ingest_path+fn)-1)) # getting the length of the path up to where glob fills in filenames

for d in dfs:
    d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")


dfs = list(map(tz_NYC, dfs))  # converting timezone by localizing to GMT then convert to NewYork

for k, v, ct in filterCriteria_0th:
  setNaN(dfs, k, v, comparetype=ct)              

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
mmaxDisplayed = 300

mmarker = dict(symbol = "circle-open",
            size = 5, 
            maxdisplayed = mmaxDisplayed)

nmarker = dict(symbol = "circle",
            size = 5)            



app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)

app.layout = html.Div([
  html.Div([
    dcc.Dropdown(
      id='yaxis-column',
      options=[{'label': i, 'value': i} for i in availablecolumns],
      value='Tdb_BME680F',
      style={'backgroundColor': colors['DDbackground'],'color': colors['text'],'box-shadow': '0px 8px 16px 0px rgba(0,0,0,0.2)' }
      ),
    dcc.Graph(
      id='Live-layout',
      #figure={'data': datatraced,'layout':layout}
    ),
    dcc.Interval(
      id='interval-component',
      interval=5*1000, # in milliseconds
      n_intervals=0
    )
  ],style={'backgroundColor': colors['background']}),
])

@app.callback(Output('Live-layout', 'figure'),
              [Input('yaxis-column', 'value'),
               Input('interval-component', 'n_intervals')])
def update_graph_live(value,n): 

    observation =  pd.read_csv(link, parse_dates=["Timestamp_Overrode"], index_col=["Timestamp_Overrode"])
    observation.index = observation.index.tz_localize('America/New_York',ambiguous='infer')

    notes= pd.DataFrame(observation[['note','sensor','Coord_X_m', 'Coord_Y_m', 'Coord_Z_m','Position_HumanReadable']])
    notes.sort_index( inplace=True )

    todaysdt = pd.to_datetime('today').tz_localize('America/New_York').strftime("%Y-%m-%d ")
    #todaysdt = pd.to_datetime('2020-01-07')
    yesterdt = (pd.to_datetime('today').tz_localize('America/New_York')-pd.Timedelta('1 day')).strftime("%Y-%m-%d ")
    #notes = notes[yesterdt:todaysdt]
    notes = notes["2020-02-01 ":"2020- "]
    



    dfs = [pd.read_csv(f, parse_dates=["timestamp"], index_col=["timestamp"]).assign(sensor=f) for f in path]
    for d in dfs:
        d["Tdb_BME680F"] = convert_temperature(d["Tdb_BME680"].dropna(), 'Celsius', 'F')
        d["Tdb_BME680F"][d["Tdb_BME680F"] < 50] = np.NaN
    dfs = list(map(tz_NYC, dfs))  # converting timezone by localizing to GMT then convert to NewYork
    



    #notes["Y"] = dfs[1][value].median()

    for d in dfs:
      d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")


    for k, v, ct in filterCriteria_0th:
      setNaN(dfs, k, v, comparetype=ct)              

    #plot
    fig = go.Figure()
    traceToPlot = [d for d in dfs]
    Valunit = list(values.unit.where(values.name == value).dropna())

    Valtitle = list(values.title.where(values.name == value).dropna())

    notes["Y"] = dfs[0][value].median()
    #locations = pd.Series(["Gym","Living Room","Kitchen","Downstairs","Upstairs"])
    #for i in range(0,5):
    #    dfs[i]["sensor"] = locations[i]

    #for i in range(len(locations)):
    #    dfs[i]["sensor"] = locations[i]

    [
    fig.add_trace(
        go.Scatter(x=d.index, y=d[value], name=d["sensor"].iloc[0],
        hoverinfo= "x+y+text+name",
        mode="markers+lines",marker = mmarker))#hovertext=d.Position_HumanReadable,
    for d in traceToPlot
    ]
    fig.add_trace(
    go.Scatter(
        x=notes.index,
        y=notes['Y'],
        name='notes',
        mode="markers",
        marker = nmarker,
        hovertext=notes.note)) 

    fig.update_layout(
    title_text=Valtitle[0],
    uirevision= value,
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
    app.run_server(debug=False, host='0.0.0.0', port = 8080)
    #app.run_server(debug=True)
