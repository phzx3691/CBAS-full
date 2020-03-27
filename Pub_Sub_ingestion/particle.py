from sensor import Sensor
import os.path
import csv
import json
import time
from time import gmtime, strftime
import numpy as np
import io
import pandas as pd
from io import StringIO
import config # from config.py
from ParticleCloud import ParticleCloud # from ParticleCloud.py
import pymysql
import sqlalchemy
import psycopg2
#from scipy.constants import convert_temperature



passwd = config.passwd  # From sqlconfig.py
user = config.user  # From sqlconfig.py
DB = 'cbas'  #name of databases to activate 

engine = sqlalchemy.create_engine('postgresql+psycopg2://'+user+':'+passwd+'@'+config.host+'/'+DB)

TOKEN = config.Particle_key

IDS = []

class Particle(Sensor):

  def login(self):

    try:
      # Function to filter out devices that should be ignored
      def good_device(device):
          device_object = getattr(self.particle_cloud, device)
          return device_object.connected and device_object.variables != None and "sensor" in device_object.variables

      IDS = self.loadDevices()

      # Retrieve connected devices
      self.particle_cloud = ParticleCloud(TOKEN, device_ids=IDS)
      self.connected_devices = list(filter(good_device, self.particle_cloud.devices))
      self.log("Info", "Identified {} connected devices".format(len(self.connected_devices)))

      entry_sensor = str(list(self.particle_cloud.devices.keys())[0])
      entry_sensor = getattr(self.particle_cloud, entry_sensor)

      entry_sensor.cloud_subscribe("Sensor", self.writeData)
      entry_sensor.cloud_subscribe("Tele", self.writeTele)

      return True

    except Exception as e:
      self.log("Error", str(e))
      return False

  def logout(self):
    return True

  def writeData(self, event_data):
    print("Wite Data")
    try:
        res = json.loads(event_data.data)
        #print("res: " + str(res))
        device = self.getDeviceName(res["coreid"])
        
        res = json.loads(res["data"])
        
        timestamp = self.getTimestamp(res)

        variables = sorted(res.keys())
        #variables.remove("epoch")
        values = list(map(lambda x: str(res[x]), variables))

        # Create header
        headers = "timestamp," + ",".join(variables) + "\n"
        data = headers + timestamp+ "," + ",".join(values)
        
        #filename = "DA-particle-" + device + "-" + self.getCurrentTime(fifteen=True) + ".csv"
        fn =  "cbas_IN-" + device + "-" + ".csv"

        start_path = self.output_dir

        filename = os.path.join(start_path, fn)
        # Strip off headers if already written to file
        ##if os.path.isfile(self.output_dir + filename): content = '\n'.join(content.split('\n')[1:])
        
        # Open output file in append mode, creates new file every day
        #f = open(self.output_dir + filename, "a")
        #f.write(content)
        #f.close()
        #Print(content)

        df = pd.read_csv(StringIO(data),header= 0,encoding='utf-8', converters={'timestamp': pd.Timestamp})
        print(device+":  ")
        print(df)
        df = df.set_index(pd.DatetimeIndex(df['timestamp']))
        df.drop('timestamp', axis=1, inplace=True)
        df['epoch'] = pd.DatetimeIndex(df['epoch'])
        df['RCO2'] = pd.to_numeric(df['RCO2'], errors='coerce')
        df['Tdb_scd30'] = pd.to_numeric(df['Tdb_scd30'], errors='coerce')
        df['RH_scd30'] = pd.to_numeric(df['RH_scd30'], errors='coerce')
        df['TVOC'] = pd.to_numeric(df['TVOC'], errors='coerce')
        df['ECO2'] = pd.to_numeric(df['ECO2'], errors='coerce')
        df['PM25'] = pd.to_numeric(df['PM25'], errors='coerce')
        df['PM1'] = pd.to_numeric(df['PM1'], errors='coerce')
        df['PM10'] = pd.to_numeric(df['PM10'], errors='coerce')
        df['PM25'] = pd.to_numeric(df['PM25'], errors='coerce')
        df['Air'] = pd.to_numeric(df['Air'], errors='coerce')
        df['Lux'] = pd.to_numeric(df['Lux'], errors='coerce')
        df['P_BME680'] = pd.to_numeric(df['P_BME680'], errors='coerce')
        df['Alt_BME680'] = pd.to_numeric(df['Alt_BME680'], errors='coerce')
        df['RH_BME680'] = pd.to_numeric(df['RH_BME680'], errors='coerce')
        df['Tdb_BME680'] = pd.to_numeric(df['Tdb_BME680'], errors='coerce')
        df['battery'] = pd.to_numeric(df['battery'], errors='coerce')
        df['sensor'] = device
        #df["Tdb_BME680F"] = convert_temperature(df["Tdb_BME680"], 'Celsius', 'F')

        def setNaN(d, key, value, comparetype):
            d[key] = d[key].where(d[key] == -99, np.NaN)
            #d[key] = d[key].where(d[key] == -98, np.NaN)
            if comparetype == "less":
                  d[key] = d[key].where(d[key] < value, np.NaN)
            if comparetype == "greater":
                  d[key] = d[key].where(d[key] > value, np.NaN)
            #else:
                  #d[key] = d[key].where(d[key] == value, np.NaN)

              


        kv = [("battery", 2, "less"),("RCO2", 400, "less"),("Tdb_scd30", 0, "less"),("Tdb_scd30", 101, "greater"),("PM25", 10000, "greater"),("Lux", 100000, "greater"),("RH_scd30", 0, "less"),("RH_scd30", 101, "greater")]
        
        #for k, v, ct in kv:
          #setNaN(df, k, v, comparetype=ct)
        #convert object to dateandtime
        #data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S')

        #print(df)
        # if file does not exist write header 
        #if not os.path.isfile((self.output_dir + filename)):
        #  df.to_csv(filename, header=True)
        #else: # else it exists so append without writing the header
        #  df.to_csv(filename, mode='a', header=False)
        #  print(filename)    
        df.to_sql('cbasdef',engine,if_exists='append',index_label='timestamp')  
        print("data-Import-2-SQL...")  
        #print("data-skipSQL...")
        with open(filename, 'a') as f:
          df.to_csv(f, mode='a', header=f.tell()==0,na_rep = "NaN")
    except Exception as e:
        self.log("Error", "Error with device {}".format(device))
        self.log("Error", str(e))

  def writeTele(self, event_data):

    try:
        res = json.loads(event_data.data)

        device = self.getDeviceName(res["coreid"])

        res = json.loads(res["data"])

        timestamp = self.getTimestamp(res)

        variables = sorted(res.keys())
        #variables.remove("epoch")
        values = list(map(lambda x: str(res[x]), variables))

        # Create header
        content = "timestamp," + ",".join(variables) + "\n"
        content = content + timestamp + "," + ",".join(values) + "\n"

        #filename = "DA-particle-" + device + "-tele-" + self.getCurrentTime(fifteen=True) + ".csv"
        df = pd.read_csv(StringIO(content),header= 0, converters={'timestamp': pd.Timestamp})
        print(device+"-Tele"+":  ")
        print(df)
        df = df.set_index(pd.DatetimeIndex(df['timestamp']))
        df.drop('timestamp', axis=1, inplace=True)
        df['epoch'] = pd.DatetimeIndex(df['epoch'])
        df['sensor'] = device
        fn = "tele-particle-" + device + ".csv"
        filename = os.path.join(self.output_dir, fn)
        # Strip off headers if already written to file
        #if os.path.isfile(filename): content = '\n'.join(content.split('\n')[1:])

        # Open output file in append mode, creates new file every day
        #f = open(self.output_dir + filename, "a")
        #f.write(content)
        #f.close()
        #df.to_sql('cbastele',engine,if_exists='append',index_label='timestamp')    
        print("tele-skipSQL...")        
        with open(filename, 'a') as f:
          df.to_csv(f, mode='a', header=f.tell()==0,na_rep = "NaN")        
    except Exception as e:
        self.log("Error", "Error with device {}".format(device))
        self.log("Error", str(e))

  # Convert epochtime to timestamp
  def getTimestamp(self, res):
    return strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime(res["epoch"]))

  def getDeviceName(self, device_id):

    device = "devise"

    for d in self.particle_cloud.devices.keys():
        s = getattr(self.particle_cloud, d)

        if(s.device_id == device_id):
            device = d
            break

    return device

  # Load device ids from particle_sensors.csv
  def loadDevices(self):

    f = open("particle_sensors.csv", "r")

    ids = []

    for i, l in enumerate(f):

      if i == 0: continue

      spl = l.split(',')

      if len(spl) < 2: continue

      ids.append(spl[0].replace('\x00', ''))

    return ids

