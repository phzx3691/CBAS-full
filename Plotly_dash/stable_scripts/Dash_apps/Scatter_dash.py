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
import plotly.express as px
import glob
from scipy import stats
import plotly.offline as offline
import flask
import statsmodels.api as sm
from tqdm import tqdm

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

#term debug
print("\033[1;32;40mImporting complete. \t\t\t\t\t\t\t\t\t\t")
print("\033[0;37;39m")

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

#set paths
samprt_path = ""'5T'""
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
start_path = os.path.join(base_path, "CSV", "2Interim","4_generateComfortMetrics")
fn = 'protoCBAS-*'
path = sorted(glob.glob(os.path.join(start_path, fn)))
values = pd.read_json(os.path.join(base_path,"values.json"))


def tz_NYC(d):
    d.index = d.index.tz_convert('America/New_York')
    #older versions of pandas will need to localize to GMT before convesion
    #d.index = d.index.tz_localize('GMT').tz_convert('America/New_York')
    return d



dfs = [pd.read_csv(f, parse_dates=["timestamp"],date_parser=lambda col: pd.to_datetime(col, utc=True), index_col=["timestamp"]).assign(sensor=f) for f in path]


# Filtering directory/file extensions
stripboard = ((len(start_path)+1)) # getting the length of the path up to where glob fills in filenames

for d in dfs:
    d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")


sensors = [d["sensor_SD"].iloc[0] for d in dfs]

dfs = list(map(tz_NYC, dfs))  # converting timezone by localizing GMT then convert to EST

#dfs = list(map(numerictimes, dfs))
availablecolumns = pd.Series(dfs[0].columns).sort_values()


#cleanup traces 
#Apply any filtering needed before plotting
[d.drop_duplicates(subset=['RCO2','Tdb_BME680'],keep = 'first', inplace = True) for d in dfs]  #remove duplicates for specific columns where sensor gets "stuck" 
dfs[1]["2019-09-05 ":"2019-11-10 "]["RCO2"] = (dfs[1]["2019-09-05 ":"2019-11-10 "]["RCO2"]-782) #adjust for gremlins in CBAS-B CO2 sensor
dfs =  [d.loc[d["Position_HumanReadable"] != '"Wind Tunnel"'] for d in dfs] # drop based on "Position_HumanReadable" column



# Define phases of time during the day / diurnal cycle
BUdata = [d.between_time('08:00', '20:00',include_start=True, include_end=True) for d in dfs]

Offdata = [d.between_time('20:01', '23:59',include_start=True, include_end=True) for d in dfs]

basedata = [d.between_time('00:00', '7:59',include_start=True, include_end=True) for d in dfs]

# How many datapoints to display per plot
mmaxDisplayed = 300

BUmarker = dict(symbol = "circle",
            size = 12,
            color = "rgb(161, 195, 221)",
            opacity = 0.6,
            line=dict(
                color='Black',
                width=1
            ),            
            maxdisplayed = mmaxDisplayed)

offmarker = dict(symbol = "circle",
            size = 12,
            color = "rgb(54, 109, 152)",
            opacity=0.5,
            line=dict(
                color='Black',
                width=1
            ),            
            maxdisplayed = mmaxDisplayed)

basemarker = dict(symbol = "circle",
            size = 12,
            color =  "rgb(33, 68, 94)",
            opacity = 0.5,
            line=dict(
                color='Black',
                width=1
            ),
            maxdisplayed = mmaxDisplayed)            


def tracevisibility(d):
  BUtrace = list(filter(lambda x: 'BU' in x, d))
  OFtrace = list(filter(lambda x: 'OF' in x, d)) 
  BStrace = list(filter(lambda x: "BS" in x, d))
  TDtrace = list(filter(lambda x: "TD" in x, d))

  if BUtrace == []:
    BUvis = False
  else:
    BUvis = True
  if OFtrace == []:
    OFvis = False
  else:
    OFvis = True    
  if BStrace == []:
    BSvis = False
  else:
    BSvis = True
  if TDtrace == []:
    TDvis = False
  else:
    TDvis = True  
  return BUvis,OFvis,BSvis,TDvis


# Fire up Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)

print("\033[1;32;40mGenerating plot. \t\t\t\t")
print("\033[0;37;39m")

# Generate XY scatter
## OPTIONS AND PARAMETERS ##
### value='RCO2',  
### value='Tdb_BME680',  

sstart_date= dfs[0].first_valid_index()
eend_date=dfs[0].last_valid_index()
#sstart_date= "2019-09-06"
#eend_date= "2019-09-24"
#Plot_wwidth = 800
#Plot_hheight = 400
#Dash inupts
x_rrange = [-0.5, 23.5]
y_rrange = [0,40]

app.layout = html.Div([
  html.Div([
    dcc.Markdown('''
      Select X-Axis:
    '''),
    dcc.Dropdown(
      id='xaxis-column',
      options=[{'label': i, 'value': i} for i in availablecolumns],
      value='Hour(EST)',#,      persistence = True
      style={'backgroundColor': colors['DDbackground'],'color': colors['text'],'box-shadow': '0px 8px 16px 0px rgba(0,0,0,0.2)' }
      )
  ],style={'width': '48%', 'display': 'inline-block'}),
  html.Div([
    dcc.Markdown('''
      Select Y-Axis:
    '''),    
    dcc.Dropdown(
      id='yaxis-column',
      options=[{'label': i, 'value': i} for i in availablecolumns],
      value='Tdb_BME680',#,       persistence = True
      style={'backgroundColor': colors['DDbackground'],'color': colors['text'],'box-shadow': '0px 8px 16px 0px rgba(0,0,0,0.2)' }
      )
  ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
  html.Div([
    dcc.Markdown('''
      Select Date Range:
    '''),    
    dcc.DatePickerRange(
      id='dt-range',
      min_date_allowed=dfs[0].first_valid_index(),
      max_date_allowed=dfs[0].last_valid_index(),  ## change to longest valid index
      start_date= sstart_date,
      end_date=eend_date,
      display_format='MMM Do, YY',
      initial_visible_month=dfs[0].first_valid_index(),
      style={'backgroundColor': colors['DDbackground'],'color': colors['text']}
    )
  ],style={'width': '48%', 'display': 'inline-block','backgroundColor': colors['DDbackground'],'color': colors['text']}),
  html.Div([
    dcc.Markdown('''
      Disable traces:
    '''),     
    dcc.Checklist(
        id='trace-show',
        options=[
          {'label':'Business hours (8AM-8PM)','value':'BU'},
          {'label':'Off Hours','value':'OF'},
          {'label':'Baseline (2AM-5AM)','value':'BS'},
          {'label':'Trendlines','value':'TD'}],
        value=['BU','OF','BS','TD'],
        style={'backgroundColor': colors['DDbackground'],'color': colors['text']},
        labelStyle={'display': 'inline-block'}#,        persistence = True
    )    
  ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
  html.Div([
      dcc.Graph(
      id='Live-layout',
      #figure={'data': datatraced,'layout':layout}
    ),
  ])
])  

@app.callback(Output('Live-layout', 'figure'),
              [Input('xaxis-column', 'value'),
                Input('yaxis-column', 'value'),
                Input('dt-range', 'start_date'),
                Input('dt-range', 'end_date'),
                Input('trace-show', 'value')])
def update_graph_live(xvalue,yvalue,start_date,end_date,traces): 

  
  
  YValunit = list(values.unit.where(values.name == yvalue).dropna())

  YValtitle = list(values.title.where(values.name == yvalue).dropna())
  
  XValunit = list(values.unit.where(values.name == xvalue).dropna())

  XValtitle = list(values.title.where(values.name == xvalue).dropna())

  #dffs = [d[datetime] for d in dfs]
  startTS = pd.Timestamp(start_date,tz='America/New_York')
  endTS = pd.Timestamp(end_date,tz='America/New_York')
  visible = tracevisibility(traces)

  if visible[3] == True:
    BUdataNA = list(map(lambda d: d[startTS:endTS].dropna(), BUdata))
    models =   [sm.OLS(d[yvalue], d[xvalue]).fit() for d in BUdataNA]
    predictions = [m.predict(d[xvalue]) for m,d in zip(models, BUdataNA)]
  else:
    BUdataNA = list(map(lambda d: d[startTS:endTS].dropna(), BUdata))
    models = []
    predictions = []



  fig = go.Figure()
  [
  fig.add_trace(
      go.Scatter(x=d[xvalue][startTS:endTS], y=d[yvalue][startTS:endTS],legendgroup=d["sensor_SD"].iloc[0],name="OH-"+d["sensor_SD"].iloc[0],
      mode="markers",marker=offmarker,
      visible=visible[1],text=d[startTS:endTS].index,
      hovertext=d.Position_HumanReadable,hoverinfo= "x+y+text+name"
      #hovertemplate ='<i>Y</i>: %{y}'+'<br>X</b>: %{x}<br>'+'Time: <b>%{text|%a %b %d, %I:%M %p}</b>'))
      ))
  for d in Offdata
  ]
  [
  fig.add_trace(
      go.Scatter(x=d[xvalue][startTS:endTS], y=d[yvalue][startTS:endTS],legendgroup=d["sensor_SD"].iloc[0],name="BS-"+d["sensor_SD"].iloc[0],
      mode="markers",marker=basemarker,visible=visible[2],text=d[startTS:endTS].index,
      hovertext=d.Position_HumanReadable,hoverinfo= "x+y+text+name"
      #hovertemplate ='<i>Y</i>: %{y}'+'<br>X</b>: %{x}<br>'+'Time: <b>%{text|%a %b %d, %I:%M %p}</b>'))
      ))
  for d in basedata
  ]
  #Business Hours Points
  [
  fig.add_trace(
      go.Scatter(x=d[xvalue][startTS:endTS], y=d[yvalue][startTS:endTS],legendgroup=d["sensor_SD"].iloc[0],name="BH-"+d["sensor_SD"].iloc[0],
      mode="markers",marker=BUmarker,visible=visible[0],text=d[startTS:endTS].index,
      hovertext=d.Position_HumanReadable, hoverinfo= "x+y+text+name",
      #hovertext=d.Position_HumanReadable+"{%a-%d %H:%M}", hoverinfo= "x+y+text+name",
      #hovertemplate = "{d.index:%c}"
      #hovertemplate ='<i>Y</i>: %{y}'+'<br>X</b>: %{x}<br>'+'Time: <b>%{d[index]:%c}</b>'
      ))
  for d  in BUdata
  ]
  [
  fig.add_trace(
      go.Scatter(x=d[xvalue], y=j,legendgroup=d["sensor_SD"].iloc[0],name="Trend-"+d["sensor_SD"].iloc[0],
      mode="lines",visible=visible[3]))
  for d,j in zip(BUdataNA, predictions)
  ]
  fig.update_layout(
      autosize=False,
      width = Plot_wwidth,
      height = Plot_hheight,
      font = {'color': colors['text'] },
      plot_bgcolor = colors['background'],
      paper_bgcolor = colors['background'],        
#      title_text=str(YValtitle[0]) + " vs. " + str(XValtitle[0]) + ". " + startTS.strftime('%b %d, %Y, %I:%M %p') + " -- " + endTS.strftime('%a %b %d, %Y, %I:%M %p'),
      title_text=str(YValtitle[0]) + " vs. " + str(XValtitle[0]) + ". " + startTS.strftime('%x') + " -- " + endTS.strftime('%x'),
      xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
          font=dict(family="Arial, Helvetica, Verdana", size=18),
          text = " (" + XValunit[0]+ ")")),
      yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
          text=" (" + YValunit[0]+ ")")
      )
  )
  #fig.update_xaxes(range=x_rrange)
  #fig.update_yaxes(range=y_rrange)

  return fig
"""  
  fig.update_layout(
      autosize=False,
      width=1500,
      height=720,      
      title_text=str(XValtitle[0])+"/ "+str(YValtitle[0])+"     "+startTS.strftime('%b %d, %Y, %I:%M %p')+" -- "+endTS.strftime('%a %b %d, %Y, %I:%M %p'),
"""
print("\033[1;32;40mFigurating. \t\t\t\t\t\t\t\t\t\t")
print("\033[0;37;39m")

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port = 8083)

