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
from src.data_processing_formatting.hipo_root_cuts.dvep_cutter import root_batch_dvpip_cutter
from src.data_processing_formatting.root_processor import root_to_txt
from src.data_processing_formatting.root_processor import txt_to_pandas

from src.data_analysis_plotting.plot_makers import make_histos
from src.data_analysis_plotting.picture_tools import prelimplot

#This is for viewing ROOT file information. The steps are:
# 1 Apply DVEP cuts to Root files
# 2 RIP root with uproot!
# 3 Convert to Pandas
# 4 Iterate the day away

###
#Function defs
###

def process_data_0():
        print("Stage 0 complete")

###

def process_data_1(root_macro,start_dir,output_dir):
    
    root_batch_dvpip_cutter.process_root_files(root_macro,start_dir,output_dir) 

    print("Stage 1 complete")

def process_data_2(data_dir,output_dir):
    
    root_to_txt.root_to_txt(data_dir,output_dir)

    print("Stage 2 complete")

def process_data_3(data_dir,output_dir):
    
    txt_to_pandas.txt_to_pandas(data_dir,output_dir)

    print("Stage 3 complete")








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
    dir_to_process = fs.data_basename 

    base_root_dir = fs.base_dir+fs.data_dir+fs.data_2_dir+dir_to_process
    output_DVEP_dir = fs.base_dir+fs.data_dir+fs.data_3_dir+dir_to_process
    output_root_txt_dir = fs.base_dir + fs.data_dir+fs.data_4_dir+dir_to_process 
    output_root_pandas_dir = fs.base_dir + fs.data_dir+fs.pandas_dir+dir_to_process 
   
    if args.start <= 0:
        process_data_0()
        print("Stage 0 complete")
    
    if args.start <=1 and args.stop >=1:
        root_macro = fs.base_dir+fs.src_dir+fs.data_processing_formatting + fs.dvep_cut_dir+fs.root_macro_script
        process_data_1(root_macro,base_root_dir,output_DVEP_dir)
        print("Stage 1 complete")

    if args.start <=2 and args.stop >=2:
        process_data_2(output_DVEP_dir,output_root_txt_dir)
        print("Stage 2 complete")
    
    if args.start <=3 and args.stop >=3:
        process_data_3(output_root_txt_dir,output_root_pandas_dir)
        print("Stage 3 complete")
