import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import random 
import sys
import os, subprocess
from pdf2image import convert_from_path
import math
from icecream import ic
import shutil
from PIL import Image, ImageDraw, ImageFont
import argparse
import time
import sys
import subprocess
import os
import json
from datetime import datetime
import shutil

#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker
from src.utils import iterators
from src.data_processing_formatting.lund_proccesor import lund_to_pandas
from src.data_processing_formatting.lund_proccesor import lund_filter
from src.data_processing_formatting.lund_proccesor import lund_event_processor



#This is for viewing LUND file information. The steps are:
# 0 - filter lund files (optional)
# 1 - Convert lund files to pandas DF
# 2 - Process lund files: calculate q2, t, phi, xb for each event
# 3 - Get 4D counts: count number of events in each 4D bin
# 4 - Plotting: Plot either 2,3, or 4 dimensionally 


fs = data_getter.filestruct()

dir_to_process = fs.lund_test_run


now = datetime.now()
dt_string = now.strftime("%Y%m%d-%H-%M")

##################################################################
##################################################################
##################################################################

filtered_lund_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.filtered_lunds + dir_to_process
filtered_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.lund_pandas_filtered + dir_to_process
evented_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.evented_lund_pandas + dir_to_process


### 1 --- convert lund files to pandas DF --- ###

lund_to_pandas.convert_lund_dir_to_dfs(filtered_lund_dir,filtered_lund_pandas_dir)

### 2 ---- process events to get q2, xb, etc ---- ###

lund_event_processor.get_events_from_lunds(filtered_lund_pandas_dir,evented_lund_pandas_dir)



# lund_to_pandas()


#  fs = data_getter.get_json_fs()
#     basedir = fs["lund_run_name"]
#     data_dir = fs["raw_data_dir"]+basedir+"lunds/"
#     data_list = os.listdir(data_dir)

#     t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+fs["raw_lund_pandas"]+basedir
#     file_maker.make_dir(t_pkl_dirpath)
        
#     for lund_file in data_list:
#         ic.disable()
#         df = convert_lund_to_df(data_dir+lund_file)
#         print("DF IS ----------")
#         print(df)  
#         df.to_pickle(t_pkl_dirpath+lund_file+".pkl")

"""

print("Running groovy analysis")

run_command = [run_groovy, groovy_script, data_location, number_of_events, number_of_files, number_of_cores, output_folder_groovy, run_message]

f_out = open(output_folder+"/"+runlog_filename, "w")
subprocess.call(run_command)#,stdout=f_out) #pipe commands to file output runlog

print("finished running analysis, now trying to do other stuff")

subprocess.call(["rm","latexoutput.log"])
"""




"""
#Path after 5_pickled_pandas/
#datafile = "F18In_168_20210129/skims-168.pkl"
datafile = "F18_Inbending_FD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-46-50.pkl"
#datafile = "F18_Inbending_CD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-54-11.pkl"

#Test iterate_2var

iter_var_bins = ["xb_ranges_clas6","q2_ranges_clas6"]

plotting_ranges = [0,360,36,0,6,20]

#iterate_2var(iter_vars,plotting_vars,iter_var_bins,
#    datafile,plotting_ranges,colorbar=False)

iter_vars = ['t','xb','q2']
plotting_vars = ['phi']
#iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
plotting_ranges = [0,360,20]

parser = argparse.ArgumentParser(description='Get Args.')
parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
args = parser.parse_args()

#set outdirs
fs = data_getter.get_json_fs()

datafile = "F18_Inbending_FD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-46-50.pkl"

plot_out_dirname = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
plot_out_dirpath = fs['base_dir']+fs['output_dir']+fs["phi_dep_dir"]+plot_out_dirname
t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+plot_out_dirname


iterate_3var(args,iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,plot_out_dir=plot_out_dirpath,t_pkl_dir=t_pkl_dirpath)





iterators.iterate_2var()

iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,colorbar=True,save_folder="pics/"
"""




# #Test iterate_4var
# iter_vars = ['phi','t','xb','q2'] 
# #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
# iter_var_bins = ["phi_ranges_clas6_14","t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]

# parser = argparse.ArgumentParser(description='Get Args.')
# parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
# args = parser.parse_args()

# #set outdirs
# fs = data_getter.get_json_fs()

# basedir = fs["lund_run_name"]
# datadir = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+fs["evented_lund_pandas"]+basedir
# datafiles = os.listdir(datadir)


# t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+fs["binned_lund_pandas"]+basedir

# dataframes = []
# for file in datafiles:

#     print(file)
#     dataframes.append(data_getter.get_dataframe(fs["evented_lund_pandas"]+basedir+file))
#     #print(dataframes[i].query("q2 > 1 & xb>0.1 & t>0.08 & phi >180"))
    
# datafile = pd.concat(dataframes)
# ic(len(datafile.query("q2 >= 1 & xb>=0.1 & t>=0.09").index))


# """
# iterators.iterate_4var(args,iter_vars,iter_var_bins,
#     datafile,t_pkl_dir=t_pkl_dirpath)
# """


# #Test iterate_3var_counts
# iter_vars = ['tmin','xBmin','Q2min']
# plotting_vars = ['phi']
# #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
# iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
# plotting_ranges = [0,360,20]

# parser = argparse.ArgumentParser(description='Get Args.')
# parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
# args = parser.parse_args()

# #set outdirs
# fs = data_getter.get_json_fs()

# datafile = fs["binned_lund_pandas"]+basedir+"pickled_counts_goodphi_new.pkl"


# plot_out_dirname = "lund_plots/"
# plot_out_dirpath = fs['base_dir']+fs['output_dir']+fs["phi_dep_dir"]+plot_out_dirname
# t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+plot_out_dirname


# iterators.iterate_3var_counts(args,iter_vars,plotting_vars,iter_var_bins,
#     datafile,plotting_ranges,plot_out_dir=plot_out_dirpath,t_pkl_dir=t_pkl_dirpath)