# TsDB  Usage

* Setup
* Connect to DB
* Table structure
* Views
* Read data from TsDB 
* Import Data

## Resources

* Learning with Kaggle
  * [Kaggle - Python](https://www.kaggle.com/learn/python)
  * [Kaggle - Pandas](https://www.kaggle.com/learn/pandas)
  * [Kaggle - SQL intro](https://www.kaggle.com/learn/intro-to-sql)

* Docs
  * [Dash/Plotly](http://dash.plotly.com/)
  * [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html#user-guide)
  * [TimescaleDB](https://docs.timescale.com/latest/introduction)
  * [SQL Tutorial](https://www.w3schools.com/sql/default.asp)
* Cheat Sheets
  * [Conda](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
  * [Pandas](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
  * [PostgreSQL through SQLAlchemy](https://www.compose.com/articles/using-postgresql-through-sqlalchemy/)


```python
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
```

    Import Complete
    

## SQL setup
create [sqlalchemy](https://docs.sqlalchemy.org/en/13/core/engines.html#postgresql) engine to connect to DB
using SQL credentials from `sqlconfig.py`

Host IP - 34.68.85.80

```python
passwd = "passwd"  # password for DB
user = "user"  # Username for DB
DB = 'cbas'  # name of database
```



```python
passwd = sqlconfig.passwd  # From sqlconfig.py
user = sqlconfig.user  # From sqlconfig.py
DB = 'cbas'  #name of databases to activate 
```


```python
print("User: "+user) # check user
```

    User: ad
    


```python
engine = sqlalchemy.create_engine('postgresql+psycopg2://'+user+':'+passwd+'@34.68.85.80/'+DB)
```

---

### DB/table structure

Databases and tables

---

```
├─cbas - (Database)
    └─ Tables
       ├── cbasdef (data from VM ingestion+(NULL)comfort metrics)
       ├── values (units and names of values for charting)
       ├── newlab(*) (NewLab data)
       ├── telemetry(*) (Telemetry data from CBAS)
```

---

### SQL VIEWS

* [Continuous Aggregates](https://docs.timescale.com/latest/api#continuous-aggregates)

* raw
  
```SQL
CREATE VIEW raw AS
SELECT "sensor","battery", "Air", "Tdb_BME680", "RH_BME680", "P_BME680", "Alt_BME680", "TVOC","ECO2", "RCO2", "Tdb_scd30", "RH_scd30", "Lux", "PM1", "PM25", "PM10"
FROM cbasdef
order by timestamp desc;
```


```python

```

## Read Data

* [TimescaleDB-"Reading data"](https://docs.timescale.com/latest/using-timescaledb/reading-data)

Just going to try pulling everythingto see what we have....


```python
query= ''' 
SELECT * 
FROM cbasdef
'''
```


```python

CBAS= pd.read_sql(query,engine,index_col=["timestamp"])
#CBAS
CBAS.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>battery</th>
      <th>Tdb_BME680</th>
      <th>RH_BME680</th>
      <th>P_BME680</th>
      <th>Alt_BME680</th>
      <th>TVOC</th>
      <th>ECO2</th>
      <th>RCO2</th>
      <th>Tdb_scd30</th>
      <th>RH_scd30</th>
      <th>...</th>
      <th>Ta_adj_fixed_air</th>
      <th>Cooling_effect_fixed_air</th>
      <th>SET_fixed_air</th>
      <th>TComf_fixed_air</th>
      <th>TempDiff_fixed_air</th>
      <th>TComfLower_fixed_air</th>
      <th>TComfUpper_fixed_air</th>
      <th>Acceptability_fixed_air</th>
      <th>Condit_fixed_air</th>
      <th>epoch</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-02-27 20:57:57+00:00</th>
      <td>4.061965</td>
      <td>23.96</td>
      <td>18.50</td>
      <td>99.69</td>
      <td>100.49</td>
      <td>90.0</td>
      <td>400.0</td>
      <td>638.0</td>
      <td>27.55</td>
      <td>15.55</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>2020-02-27 20:58:59+00:00</th>
      <td>4.061965</td>
      <td>23.97</td>
      <td>18.49</td>
      <td>99.69</td>
      <td>100.66</td>
      <td>92.0</td>
      <td>400.0</td>
      <td>636.0</td>
      <td>27.57</td>
      <td>15.60</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>2020-02-27 21:00:01+00:00</th>
      <td>4.059721</td>
      <td>23.98</td>
      <td>18.58</td>
      <td>99.69</td>
      <td>100.49</td>
      <td>87.0</td>
      <td>400.0</td>
      <td>640.0</td>
      <td>27.56</td>
      <td>15.69</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>2020-02-27 21:01:02+00:00</th>
      <td>4.072067</td>
      <td>23.98</td>
      <td>18.58</td>
      <td>99.69</td>
      <td>100.49</td>
      <td>88.0</td>
      <td>400.0</td>
      <td>644.0</td>
      <td>27.59</td>
      <td>15.71</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>2020-02-27 21:02:04+00:00</th>
      <td>4.065333</td>
      <td>23.99</td>
      <td>18.61</td>
      <td>99.69</td>
      <td>101.16</td>
      <td>103.0</td>
      <td>400.0</td>
      <td>650.0</td>
      <td>27.59</td>
      <td>15.66</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaT</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 58 columns</p>
</div>




```python
# What sensors do we have?
CBAS['sensor'].unique()
```




    array(['BEEM-A', 'BEEM-C', 'BEEM-D', 'Moe', 'protoCBAS-G', 'protoCBAS-B',
           '84N_Coronoffice'], dtype=object)



### More Queries

#### From Now() to interval
* Starting now() go back to `[interval]`:
```SQL
SELECT * 
FROM [table]
WHERE timestamp > NOW() - interval '[interval]';
```


```python
query = '''
SELECT * 
FROM cbasdef
WHERE timestamp > NOW() - interval '1 hour';
'''
```


```python
CBAS = pd.read_sql(query,engine,index_col=["timestamp"])
#CBAS
CBAS.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>battery</th>
      <th>Tdb_BME680</th>
      <th>RH_BME680</th>
      <th>P_BME680</th>
      <th>Alt_BME680</th>
      <th>TVOC</th>
      <th>ECO2</th>
      <th>RCO2</th>
      <th>Tdb_scd30</th>
      <th>RH_scd30</th>
      <th>...</th>
      <th>Ta_adj_fixed_air</th>
      <th>Cooling_effect_fixed_air</th>
      <th>SET_fixed_air</th>
      <th>TComf_fixed_air</th>
      <th>TempDiff_fixed_air</th>
      <th>TComfLower_fixed_air</th>
      <th>TComfUpper_fixed_air</th>
      <th>Acceptability_fixed_air</th>
      <th>Condit_fixed_air</th>
      <th>epoch</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-02 16:24:41+00:00</th>
      <td>4.045130</td>
      <td>24.04</td>
      <td>25.52</td>
      <td>100.13</td>
      <td>63.91</td>
      <td>103.0</td>
      <td>400.0</td>
      <td>500.0</td>
      <td>27.10</td>
      <td>22.13</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:24:38+00:00</th>
      <td>4.079924</td>
      <td>24.46</td>
      <td>28.66</td>
      <td>100.13</td>
      <td>63.91</td>
      <td>186.0</td>
      <td>400.0</td>
      <td>711.0</td>
      <td>27.12</td>
      <td>25.54</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:24:29+00:00</th>
      <td>4.045130</td>
      <td>24.04</td>
      <td>25.78</td>
      <td>100.13</td>
      <td>63.74</td>
      <td>102.0</td>
      <td>400.0</td>
      <td>503.0</td>
      <td>27.13</td>
      <td>21.80</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:24:28+00:00</th>
      <td>4.074312</td>
      <td>24.90</td>
      <td>35.11</td>
      <td>100.51</td>
      <td>32.07</td>
      <td>354.0</td>
      <td>400.0</td>
      <td>1148.0</td>
      <td>26.50</td>
      <td>33.34</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:24:18+00:00</th>
      <td>4.023804</td>
      <td>24.03</td>
      <td>25.88</td>
      <td>100.13</td>
      <td>63.57</td>
      <td>107.0</td>
      <td>403.0</td>
      <td>506.0</td>
      <td>27.10</td>
      <td>22.13</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 58 columns</p>
</div>



#### SELECT sensor(s)
* select sensor:
```SQL
SELECT * FROM cbasdef
WHERE sensor IN ('Moe','BEEM-A')
AND timestamp > NOW() - interval '1 hour';
```


```python
query = '''
SELECT * FROM cbasdef
WHERE sensor IN ('Moe')
AND timestamp > NOW() - interval '1 hour';
'''
```


```python
CBAS = pd.read_sql(query,engine,index_col=["timestamp"])
#CBAS
CBAS.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>battery</th>
      <th>Tdb_BME680</th>
      <th>RH_BME680</th>
      <th>P_BME680</th>
      <th>Alt_BME680</th>
      <th>TVOC</th>
      <th>ECO2</th>
      <th>RCO2</th>
      <th>Tdb_scd30</th>
      <th>RH_scd30</th>
      <th>...</th>
      <th>Ta_adj_fixed_air</th>
      <th>Cooling_effect_fixed_air</th>
      <th>SET_fixed_air</th>
      <th>TComf_fixed_air</th>
      <th>TempDiff_fixed_air</th>
      <th>TComfLower_fixed_air</th>
      <th>TComfUpper_fixed_air</th>
      <th>Acceptability_fixed_air</th>
      <th>Condit_fixed_air</th>
      <th>epoch</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-02 16:24:43+00:00</th>
      <td>4.125942</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:24:12+00:00</th>
      <td>4.125942</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:23:41+00:00</th>
      <td>4.136044</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:23:09+00:00</th>
      <td>4.136044</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
    <tr>
      <th>2020-04-02 16:22:38+00:00</th>
      <td>4.123698</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>-99.0</td>
      <td>...</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>1970-01-01 00:00:01.585844</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 58 columns</p>
</div>



#### time_buckets ([pd.resample](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html)) 

* [TimescaleDB-"time_bucket()"](https://docs.timescale.com/latest/api#time_bucket)

* [TimescaleDB-Blog](https://blog.timescale.com/blog/simplified-time-series-analytics-using-the-time_bucket-function/)

Example for avg temp in the last hour resampled by 5min:
```SQL
SELECT time_bucket('5 minutes', timestamp) AS five_min,
AVG("Tdb_BME680") as temp,
sensor as sensor
FROM raw
WHERE sensor IN ('protoCBAS-G')
AND timestamp > NOW() - interval '1 hour'
GROUP BY five_min, sensor;
```





```python
query = '''
SELECT time_bucket('5 minutes', timestamp) AS five_min,
AVG("Tdb_BME680") as temp,
sensor as sensor
FROM raw
WHERE sensor IN ('protoCBAS-G')
AND timestamp > NOW() - interval '1 hour'
GROUP BY five_min, sensor;
'''
```


```python
CBAS = pd.read_sql(query,engine,index_col=["five_min"])
CBAS
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>temp</th>
      <th>sensor</th>
    </tr>
    <tr>
      <th>five_min</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-02 17:00:00+00:00</th>
      <td>24.770000</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:45:00+00:00</th>
      <td>24.828750</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:55:00+00:00</th>
      <td>24.790000</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:40:00+00:00</th>
      <td>24.851111</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:35:00+00:00</th>
      <td>24.871111</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 17:05:00+00:00</th>
      <td>24.755000</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:30:00+00:00</th>
      <td>24.880000</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:10:00+00:00</th>
      <td>24.962222</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:15:00+00:00</th>
      <td>24.918889</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:50:00+00:00</th>
      <td>24.805556</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:25:00+00:00</th>
      <td>24.895556</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:05:00+00:00</th>
      <td>25.013333</td>
      <td>protoCBAS-G</td>
    </tr>
    <tr>
      <th>2020-04-02 16:20:00+00:00</th>
      <td>24.906250</td>
      <td>protoCBAS-G</td>
    </tr>
  </tbody>
</table>
</div>



## Other SQL tools




* [pgadmin](https://www.pgadmin.org/)
![](../assets/Pgadmin1.jpg)

* [Graphana](https://grafana.com/)
