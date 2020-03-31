
import numpy as np
import pandas as pd
import os.path
from datetime import datetime
import glob
from tqdm import tqdm


samprt = ""'5T'""


#set paths
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("base: " +base_path)


start_path = os.path.join(base_path, "CSV", "SDcard", "processed", "merged", "resampled", "resampled(" + samprt + ")")
#print("start: " + start_path)
final_path_out = os.path.join(start_path, "extratest")
#print("final: " + final_path_out)
home_path = os.path.dirname(os.path.dirname(base_path))
ingest_path = os.path.join(home_path,"ingest","sensor-feed","csv")
#fn = 'protoCBAS-*'
fn = 'cbas_IN-*'   # CSVs from ingestion start
path = glob.glob(os.path.join(ingest_path, fn)) 

print("path: "+ str(path))

