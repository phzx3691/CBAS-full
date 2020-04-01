import sys
import json
from time import gmtime, strftime
import os.path
import glob
import pandas as pd
from tqdm import tqdm



if len(sys.argv) < 2:
  print("Usage: python SDparse_copy.py [Board]")
  sys.exit(1)

board = sys.argv[1]
#in_path = os.path.join(sys.argv[2],board)
#out_path = os.path.join(sys.argv[2], "processed", "merged","test")

# currently available board names
# protoCBAS-A
# protoCBAS-B
# protoCBAS-C
# protoCBAS-D
# protoCBAS-G


#set paths
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fnout = "cbas_post_SD_"+board+".csv"
out_path = os.path.join(base_path, "CSV", "2Interim", "1_SD_pandas_parse_")
final_path_out = os.path.join(out_path, fnout)

fn = 'cbas*.csv'
in_path = os.path.join(base_path, "CSV", "3Raw", "From_SDcard",board)
final_path_in = sorted(glob.glob(os.path.join(in_path, fn))) #read everything in folder matching fn to list of each directory

print("Found Paths:")
print(final_path_in)



def loadJSONDataFrames(fns):
  return list(map(lambda f: pd.read_json(f,lines=True,convert_dates='epoch',date_unit ='s'), fns))
  # parse_dates=["epoch"], index_col=["epoch"] )
  #read.csv while converting timestamp and setting to index.


def setIndex(d):
  d = d.set_index((pd.to_datetime(d['epoch'],unit='s')))
  d.index = d.index.tz_localize('UTC',ambiguous='infer')
  #d = d.tz_convert('America/New_York')
  return d


cbas = loadJSONDataFrames(final_path_in)

cbas_indx= list(map(setIndex, cbas))  # converting timezone and setting timestamp to index. not needed w tz_NYC def


df = pd.concat(cbas_indx)
df.sort_index( inplace=True )




#print("Saving to CSV:" + final_path_out)


df.to_csv(final_path_out, index_label='timestamp')


print("Done")
