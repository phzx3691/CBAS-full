import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as FF
import plotly.offline as offline
from datetime import datetime
import glob
import os.path
import pymysql
import sqlconfig # From sqlconfig.py
import pandas as pd
import sqlalchemy
import psycopg2
from tqdm import tqdm
print("Import Complete")


#################################### to config file #################################################################



def tz_NYC(d): #timezone conversion
    for key in d.values():
        key.index = key.index.tz_convert('America/New_York')
    return d


def CtoF(dataframes):
    for d in dataframes.values():
        d["Tdb_BME680F"] = convert_temperature(d["Tdb_BME680"].dropna(), 'Celsius', 'F')

def setNaN(dataframes, key, value, comparetype="less"):
       for d in dataframes.values():
           if comparetype == "less":
               d[key][d[key] < value] = np.NaN
           elif comparetype == "greater":
               d[key][d[key] > value] = np.NaN
           else:
               d[key][d[key] == value] = np.NaN


ttickformatstops=[
    go.layout.xaxis.Tickformatstop(
        dtickrange=[None, 1000], value="%e-%b <br> %a <br> %I:%M:%S.%L %p"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[1000, 60000], value="%e-%b <br> %a <br> %I:%M:%S %p"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[60000, 3600000], value="%e-%b <br> %a <br> %I:%M %p"),
    go.layout.xaxis.Tickformatstop(
        dtickrange=[3600000, 86400000], value="%e-%b <br> %a <br> %I:%M %p"),
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


filterCriteria_0th = [("battery", 2, "less"), ("RCO2", 0, "less"),
                      ("RCO2", 5000, "greater"), ("Tdb_BME680", 0, "less"),
                      ("Tdb_scd30", 0, "less"), ("Tdb_scd30", 101, "greater"),
                      ("PM25", 5000, "greater"), ("PM25", 0, "less"),
                      ("Lux", 100000, "greater"), ("RH_scd30", 0, "less"),
                      ("RH_scd30", 101, "greater"), ("RH_BME680", 0, "less"),
                      ("RH_BME680", 101, "greater"), ("Air", 20, "greater"),
                      ("TVOC", 0, "less"),("Lux", 0, "less"),("P_BME680", 0, "less"),
                      ("Alt_BME680", 0, "less")]


#set number of points that shows up on a plot. set to 0 for all of the points
mmaxDisplayed = 300

mmarker = dict(symbol = "circle-open",
            size = 5, 
            maxdisplayed = mmaxDisplayed)

nmarker = dict(symbol = "circle",
            size = 5)            


#################################### to config file #################################################################


######### SQL setup
passwd = sqlconfig.passwd  # From sqlconfig.py
user = sqlconfig.user  # From sqlconfig.py
DB = 'cbas'  #name of databases to activate 

engine = sqlalchemy.create_engine('postgresql+psycopg2://'+user+':'+passwd+'@34.68.85.80/'+DB)
######### SQL setup  ####needs ADJUSTMENST FOR HOST


server = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#start_path = '/home/sheldon/ingest/sensor-feed/csv/'


Plot_wwidth = 700
Plot_hheight = 900


colors = {
    'background': '#303030', #black
    'DDbackground': '#303030', #
    'DDtext': '#FFFFFF', 
    'text': '#FFFFFF'  
}

'''
colors = {
    'background': '#FFFFFF', #white
    'text': '#000000'
}
'''



link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5JRPuanz8kRkVKU6BsZReBNENKglrLQDj1CTWnM1AqpxdWdWb3BEEzSeIcuPq9rSLNwzux_1l7mJb/pub?gid=1668794547&single=true&output=csv'
'''


observation =  pd.read_csv(link, parse_dates=["Timestamp_Overrode"], index_col=["Timestamp_Overrode"])
observation.index = observation.index.tz_localize('America/New_York',ambiguous='infer')

notes= pd.DataFrame(observation[['note','sensor','Coord_X_m', 'Coord_Y_m', 'Coord_Z_m','Position_HumanReadable']])
notes.sort_index( inplace=True )
notes = notes["2020-01-01 ":"2020- "]
'''

queryv = '''
SELECT * 
FROM values;
'''

values = pd.read_sql(queryv,engine)


query = '''
SELECT * 
FROM raw
WHERE timestamp > NOW() - interval '1 hour';
'''

dfbuff = pd.read_sql(query,engine,index_col=["timestamp"])

sensors = dfbuff.sensor.unique()
print(sensors)


dfs = {}

for s in sensors:
    dfs[s] = dfbuff.where(dfbuff["sensor"] == s).dropna()


availablecolumns = pd.Series(list(dfs.values())[0].columns).sort_values()
