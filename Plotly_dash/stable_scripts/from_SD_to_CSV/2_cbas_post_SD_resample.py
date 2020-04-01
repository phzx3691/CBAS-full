# script to pull csv data that has been concat using SD_pandas_parse_.py
# points to directory containing multiple csv files, for each board
# resamples per "samprt" and saves csv
# to be further processed

import sys
import numpy as np
import pandas as pd
import os.path
from datetime import datetime
import glob
from tqdm import tqdm



if len(sys.argv) < 2:
  print("Usage: python 2_cbas_post_SD_resample.py [sample rate]")
  sys.exit(1)

samprt = sys.argv[1]
#samprt = ""'5T'""


#set paths
samprt_path = 'resampled('+samprt+')'
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

final_path_out = os.path.join(base_path,"2Interim","2_cbas_post_SD_resample",samprt_path)


#set paths
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

final_path_out = os.path.join(base_path,"CSV","2Interim","2_cbas_post_SD_resample",samprt_path)


fn = 'cbas_post_SD_*'  
in_path = os.path.join(base_path, "CSV", "2Interim", "1_SD_pandas_parse_")
final_path_in = sorted(glob.glob(os.path.join(in_path, fn))) #read everything in folder matching fn to list of each directory

print("Found Paths:")
print(final_path_in)

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



dfs = [pd.read_csv(f, parse_dates=["timestamp"], index_col=["timestamp"]).assign(sensor=f) for f in tqdm(final_path_in,desc="Reading CSVs...")]
dfs = list(map(lambda d: d.drop(columns =['epoch']), dfs))  #drop epoch column
availablecolumns = pd.Series(dfs[0].columns)

stripboard = ((len(in_path+fn))) # getting the length of the path up to where glob fills in filenames

for d in dfs:
    d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")

sensors = [d["sensor"][0] for d in dfs]

print(sensors)
print([d.shape for d in dfs])

for k, v, ct in filterCriteria_0th:
 setNaN(dfs, k, v, comparetype=ct)   


#####cut wind tunnel

filins = {
    'Air': 0,
    'PM25': 0,
    'PM10': 0
}

dfs = list(
    map(lambda d: d.fillna(filins),
        dfs))  # fill in 0 for NaN values, as of now this is only Air col


sensors = [d["sensor"][0] for d in dfs]



samp_dfs = list(map(lambda d: d.resample(samprt).mean(), dfs))



for i in tqdm(range(len(samp_dfs)),desc="Writing CSVs..."):
    samp_dfs[i].to_csv(os.path.join(final_path_out,sensors[i]+".csv"))

print("done! " + "sample rate-"+samprt)