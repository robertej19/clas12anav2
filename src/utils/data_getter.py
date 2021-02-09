import pandas as pd
import json
from icecream import ic


def get_json_fs():
    json_file = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/src/file_structure.json"
    with open(json_file) as f:
        fs = json.load(f)
    return fs

def get_dataframe(pickled_df_file):
	fs = get_json_fs()
	datadir = fs["base_dir"]+fs["data_dir"]+fs["pandas_dir"]

	df = pd.read_pickle(datadir+pickled_df_file)
	ic(df.shape)
	return df