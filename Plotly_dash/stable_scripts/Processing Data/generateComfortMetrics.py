import os
import glob
import numpy as np
import pandas as pd
from datetime import datetime
import comfort_models
from tqdm import tqdm
from datetime import datetime

print("No swifter Start Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# Comfort defaults
MRT = 25
MET = 1.1
CLO = 0.65
FIXED_AIR = 1.2

# Set up paths
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

comf_path = os.path.join(base_path, "comfort")

weather_file = "HWD_NYC_2000-2019 openweathermap e22c8df227dc0163851cfde04816829e.csv"
weather_path = os.path.join(base_path, "HWData", weather_file)

samprt_path = ""'5T'"" 
start_path = os.path.join(base_path, "CSV", "2Interim", "3_extradata")

final_path_out = os.path.join(base_path, "CSV", "2Interim", "4_generateComfortMetrics")

# Read everything in folder matching fn to list of each directory
fn = 'protoCBAS-*'
path = sorted(glob.glob(os.path.join(start_path, fn)))

print("Reading csvs from " + start_path)

# Read sensors into a list of data frames
dfs = [pd.read_csv(f, parse_dates=["timestamp"], index_col=["timestamp"]).assign(sensor=f) for f in tqdm(path,desc="Reading CSVs...")]
availablecolumns = pd.Series(dfs[0].columns)

print("Loaded sensor data for " + str(len(dfs)) + " sensors")

# Load and process historical weather data
weather_data = pd.read_csv(weather_path, usecols=['dt', 'temp'])
weather_data = weather_data.drop_duplicates()
weather_data['dt'] = pd.to_datetime(weather_data['dt'], unit='s')
weather_data = weather_data.set_index('dt')
weather_data = weather_data.resample('D').mean()

# Function to calculate the average temperature of 30 days prior to the given timestamp
def runningMean(row):

    end_date = row.name
    start_date = row.name - np.timedelta64(30, 'D')

    thirty_days = weather_data.loc[start_date:end_date]
    range_mean = thirty_days['temp'].mean()

    return range_mean

# Filtering directory/file extensions
stripboard = ((len(start_path))) # getting the length of the path up to where glob fills in filenames

for d in dfs:
    d.sensor = d.sensor.str.slice(start=stripboard).str.replace(".csv", "")

sensors = [d["sensor_SD"][0] for d in dfs]
shape = [d.shape for d in dfs]

# Apply comfort functions
for i, d in enumerate(dfs):
    print("Performing comfort calculations on sensor " + sensors[i])
    tqdm.pandas(desc="Performing comfort calculations on sensor " + sensors[i])
    # comfUTCI
    d[['UTCI_approx', 'UTCI_comfortable', 'UTCI_stressRange']] = d.progress_apply(lambda x: comfort_models.comfUTCI(x['Tdb_BME680'], MRT, x['Air'], x['RH_BME680']), axis=1, result_type='expand')

    # comfPMVElevatedAirspeed
    d[['PMV', 'PPD', 'Ta_adj', 'Cooling_effect', 'SET']] = d.progress_apply(lambda x: comfort_models.comfPMVElevatedAirspeed(x['Tdb_BME680'], MRT, x['Air'], x['RH_BME680'], MET, CLO), axis=1, result_type='expand')

    # comfAdaptiveComfortASH55
    d['running_mean'] = d.progress_apply(runningMean, axis=1)
    d[['TComf', 'TempDiff', 'TComfLower', 'TComfUpper', 'Acceptability', 'Condit']] = d.progress_apply(lambda x: comfort_models.comfAdaptiveComfortASH55(x['Tdb_BME680'], MRT, x['running_mean'], x['Air']), axis=1, result_type='expand')

    # comfUTCI fixed air speed
    d[['UTCI_approx_fixed_air', 'UTCI_comfortable_fixed_air', 'UTCI_stressRange_fixed_air']] = d.progress_apply(lambda x: comfort_models.comfUTCI(x['Tdb_BME680'], MRT, FIXED_AIR, x['RH_BME680']), axis=1, result_type='expand')

    # comfPMVElevatedAirspeed fixed air speed
    d[['PMV_fixed_air', 'PPD_fixed_air', 'Ta_adj_fixed_air', 'Cooling_effect_fixed_air', 'SET_fixed_air']] = d.progress_apply(lambda x: comfort_models.comfPMVElevatedAirspeed(x['Tdb_BME680'], MRT, FIXED_AIR, x['RH_BME680'], MET, CLO), axis=1, result_type='expand')

    # comfAdaptiveComfortASH55 fixed air speed
    d['running_mean'] = d.progress_apply(runningMean, axis=1)
    d[['TComf_fixed_air', 'TempDiff_fixed_air', 'TComfLower_fixed_air', 'TComfUpper_fixed_air', 'Acceptability_fixed_air', 'Condit_fixed_air']] = d.progress_apply(lambda x: comfort_models.comfAdaptiveComfortASH55(x['Tdb_BME680'], MRT, x['running_mean'], FIXED_AIR), axis=1, result_type='expand')

print("Writing csvs")

# Write csvs
for i in tqdm(range(len(dfs)),desc="Writing CSVs..."):
    dfs[i].to_csv(os.path.join(final_path_out, sensors[i] + ".csv"), index_label="timestamp")

print("Finished, see the following path for results:")
print(final_path_out)

print("End Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

