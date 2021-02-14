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
from src.utils import filestruct
from src.utils import query_maker
from src.utils import file_maker
from src.utils import iterators
from src.data_processing_formatting.lund_proccesor import lund_to_pandas
from src.data_processing_formatting.lund_proccesor import lund_filter
from src.data_processing_formatting.lund_proccesor import lund_event_processor
from src.data_analysis_plotting.plot_makers import make_histos


#This is for viewing LUND file information. The steps are:
# 0 - filter lund files (optional)
# 1 - Convert lund files to pandas DF
# 2 - Process lund files: calculate q2, t, phi, xb for each event
# 3 - Get 4D counts: count number of events in each 4D bin
# 4 - Plotting: Plot either 2,3, or 4 dimensionally 


def process_lunds0():
    print("not yet implemanted")

def process_lunds1(filtered_lund_dir,filtered_lund_pandas_dir):
    ### 1 --- convert lund files to pandas DF --- ###

    lund_to_pandas.convert_lund_dir_to_dfs(filtered_lund_dir,filtered_lund_pandas_dir)


def process_lunds2(filtered_lund_pandas_dir,evented_lund_pandas_dir):
 
    ### 2 ---- process events to get q2, xb, etc ---- ###

    lund_event_processor.get_events_from_lunds(filtered_lund_pandas_dir,evented_lund_pandas_dir)

def make_2d_q2_xb_plot(combined_df,saveplot=False):
    #### At this point we can make histograms if we would like ####

    x_data = combined_df["xb"]
    y_data = combined_df["q2"]
    var_names = ["xB","Q^2"]
    ranges = [0,1,100,0,12,120]
    lund_q2_xb_title = "Q2 vs xB for {}".format(dir_to_process)

    make_histos.plot_2dhist(x_data,y_data,var_names,ranges,colorbar=True,
                saveplot=saveplot,pics_dir=outputs_dir,plot_title=lund_q2_xb_title.replace("/",""))


def process_lunds3(args,df,out_dir,pkl_outname):
    ### 3 ---- Now count how many events are in each 4D bin and return appropriate DF ---- ###

    iter_vars = ['phi','t','xb','q2'] 
    iter_var_bins = ["phi_ranges_clas6_14","t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]

    iterators.iterate_4var(args,iter_vars,iter_var_bins,
        df,t_pkl_dir=out_dir,pkl_filename=pkl_outname)



now = datetime.now()
dt_string = now.strftime("%Y%m%d-%H-%M")

##################################################################
##################################################################
##################################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    parser.add_argument('-s','--start', type=int, help='hop in point of program',default=1)
    parser.add_argument('-p','--stop', type=int,help='hop out point of program',default=3)
    parser.add_argument('-i','--hist1',help='make q2 vs xb graph',default=False,action="store_true")
    args = parser.parse_args()

    fs = filestruct.fs()
    dir_to_process = fs.lund_test_run
    outputs_dir = fs.base_dir+fs.output_dir + fs.lund_outputs

    raw_data_dir = "/mnt/d/CLAS12Data/sims_q2_w_cut/"
    filtered_lund_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.filtered_lunds + dir_to_process
    filtered_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.lund_pandas_filtered + dir_to_process
    evented_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.evented_lund_pandas + dir_to_process
    counted_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.binned_lund_pandas + dir_to_process
    counted_pickled_out_name = fs.counted_pickled_out_name

    start_dir = raw_data_dir + dir_to_process

    if args.start <= 0:
        process_lunds0()
    
    if args.start <=1 and args.stop >=1:
        process_lunds1(start_dir,filtered_lund_pandas_dir)
    
    if args.start <=2 and args.stop >=2:
        process_lunds2(filtered_lund_pandas_dir,evented_lund_pandas_dir)

    data_list = os.listdir(evented_lund_pandas_dir)
    dataframes = []
    for file in data_list:
        print(file)
        dataframes.append(pd.read_pickle(evented_lund_pandas_dir+file))
    combined_lund_df = pd.concat(dataframes)

    if args.hist1:
        make_2d_q2_xb_plot(combined_lund_df,saveplot=True)

    if args.start <=3 and args.stop >=3:
        process_lunds3(args,combined_lund_df,counted_lund_pandas_dir,counted_pickled_out_name)



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