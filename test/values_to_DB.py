import numpy as np
import pandas as pd
import os.path
from datetime import datetime
import glob
import sqlconfig # From sqlconfig.py
import sqlalchemy
import psycopg2
print("Import Complete")




base_path = os.getcwd()
print(" Base Path: " + base_path)

path = os.path.join(base_path,"Documents", "GitHub","CBAS-full")
valuefile = os.path.abspath(os.path.join(path,"values.json"))

values = pd.read_json(valuefile)

passwd = sqlconfig.passwd  # From sqlconfig.py
user = sqlconfig.user  # From sqlconfig.py
DB = 'cbas'  #name of databases to activate 

engine = sqlalchemy.create_engine('postgresql+psycopg2://'+user+':'+passwd+'@34.68.85.80/'+DB)


print(engine.table_names())

values.to_sql('values',engine,if_exists='append',index=False)
print("FINITO")