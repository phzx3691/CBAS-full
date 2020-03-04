#merges observational notation from Gsheet link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5JRPuanz8kRkVKU6BsZReBNENKglrLQDj1CTWnM1AqpxdWdWb3BEEzSeIcuPq9rSLNwzux_1l7mJb/pub?gid=1668794547&single=true&output=csv'

import sys
import numpy as np
import pandas as pd
import os.path
from datetime import datetime
import glob
from scipy import stats
from tqdm import tqdm


if len(sys.argv) < 2:
  print("Usage: python 3_extradata.py [sample rate]")
  sys.exit(1)

samprt = sys.argv[1]
#samprt = ""'5T'""



link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5JRPuanz8kRkVKU6BsZReBNENKglrLQDj1CTWnM1AqpxdWdWb3BEEzSeIcuPq9rSLNwzux_1l7mJb/pub?gid=1668794547&single=true&output=csv'


#observation =  pd.read_csv(link)
observation =  pd.read_csv(link, parse_dates=["Timestamp_Overrode"], index_col=["Timestamp_Overrode"])
observation.index = observation.index.tz_localize('America/New_York').tz_convert('UTC')

notes= pd.DataFrame(observation[['note','sensor','Coord_X_m', 'Coord_Y_m', 'Coord_Z_m','Position_HumanReadable']])
notes.sort_index( inplace=True )
notes = notes["2019-09-05 ":"2019-12-10 "]

#set paths
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("base: " +base_path)
start_path = os.path.join(base_path, "CSV", "2Interim", "2_cbas_post_SD_resample","resampled(" + samprt + ")")
print("start: " + start_path)
final_path_out = os.path.join(base_path, "CSV", "2Interim", "3_extradata")
print("final: " + final_path_out)
fn = 'protoCBAS-*'
path = sorted(glob.glob(os.path.join(start_path, fn)))
#print("path: "+ str(path))


dfs = [pd.read_csv(f, parse_dates=["timestamp"], index_col=["timestamp"]).assign(sensor=f) for f in tqdm(path,desc="Reading CSVs...")]
availablecolumns = pd.Series(dfs[0].columns)

print("Loaded sensor data for " + str(len(dfs)) + " sensors")


## filtering directory/file extensions
stripboard = ((len(start_path)+1)) # getting the length of the path up to where glob fills in filenames

for d in dfs:
    d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")

sensors = [d["sensor"][0] for d in dfs]
shape = [d.shape for d in dfs]
print("From file ---"+str(sensors))
print(" df shape ---"+str(shape))


dfsNoted = [pd.merge(d,notes.where(notes.sensor.str.contains(d["sensor"][1]))
    ,left_index=True, right_index=True, how = 'outer',suffixes=('_SD', '_note')) for d in tqdm(dfs,desc="Merging notes...")]



# limit for forward fill so big gaps dont have unessesary metadata
# may need to adjust with different ranges/samplerates/gaps

#1440 m in 24 hrs

#720 in 12hrs

#144 5Ts in 720

#24 30Ts in 720

#144 5Ts in 1440

#24 30Ts in 1440

ffilllimit = None

# maximum number of consecutive NaN values to forward/backward fill. 
# In other words, if there is a gap with more than this number of consecutive NaNs,
# it will only be partially filled.


dfsNoted_ffill = [d.fillna(method='ffill',limit=ffilllimit) for d in tqdm(dfsNoted,desc="ffill...")]



for i in range(len(dfsNoted)):
    dfsNoted[i][['sensor_SD', 'note', 'sensor_note', 'Coord_X_m', 'Coord_Y_m',
        'Coord_Z_m', 'Position_HumanReadable']] = dfsNoted_ffill[i][['sensor_SD', 'note', 'sensor_note', 'Coord_X_m', 'Coord_Y_m',
        'Coord_Z_m', 'Position_HumanReadable']]
#idea is to ff/bf only these columns and not sensor data

dfsNoted_sensorbfill = [d.fillna(method='bfill') for d in tqdm(dfsNoted,desc="bfill...")] # fill sensor colums up to 0

for i in range(len(dfsNoted)):
    dfsNoted[i][['sensor_SD','sensor_note']] = dfsNoted_sensorbfill[i][['sensor_SD','sensor_note']]

def numerictimes(d):
    d['Wkdy(EST)'] = pd.to_numeric(d.index.tz_convert('America/New_York').strftime('%w'))
    d['Hour(EST)'] = pd.to_numeric(d.index.tz_convert('America/New_York').strftime('%H'))
    d['Month(EST)'] = pd.to_numeric(d.index.tz_convert('America/New_York').strftime('%m'))
    d['TOD(EST)'] = pd.to_numeric(d.index.tz_convert('America/New_York').strftime('%H''%M'))
    d['DOY(EST)'] = pd.to_numeric(d.index.tz_convert('America/New_York').strftime('%j'))
    #d['DWkdy(EST)'] = pd.to_numeric(d.index.tz_convert('America/New_York').strftime('%w'))
    return d


print("Numeric time colums....")
#dfsNoted = list(map(numerictimes, dfsNoted))

dfsNoted = [numerictimes(d) for d in tqdm(dfsNoted,desc="Numeric time...")]

for i in tqdm(range(len(dfsNoted)),desc="Writing CSVs..."):
    dfsNoted[i].to_csv(os.path.join(final_path_out,sensors[i]+".csv"),index_label="timestamp")



dfsensors = [d["sensor_SD"][0] for d in dfsNoted]
notessensors = [d["sensor_note"][0] for d in dfsNoted]

print("From DF ---"+str(dfsensors))
print("From Note ---"+str(notessensors))
print("done! " + "sample rate-"+samprt)