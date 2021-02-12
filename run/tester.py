from matplotlib.colors import LinearSegmentedColormap
import numpy as np
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

#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker
from src.penana.plot_makers import make_histos
from src.penana.picture_tools import prelimplot


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    args = parser.parse_args()

    fs = data_getter.get_json_fs()
    # datafile = fs["test_run_dir"]+fs["phi_fits_pkl_name"]
    # data = data_getter.get_dataframe(datafile)
    # ic(data)

    # for i in data["A_uncert"]:
    #     if i >0:
    #         print(i)

    # ic(asw)

    # sys.exit()

    t_texts = fs["t_ranges_clas6_14"]

    plot_out_dirname = fs["test_run_dir"]
    dirname = fs['base_dir']+fs['output_dir']+fs["t_dep_dir"]+plot_out_dirname

    dirs = ["t00","t01","t02","t03","t04","t05","t06","t07","t08","t09","t10","t11","t12"]
    #dirs = ["t02",]
    dirbase = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/phi_1d_hists/test_pickler/"
    savedir = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/tempouters/"
    #dirbase = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/phi_1d_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/"
    #dirbase = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/phi_1d_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/t00 "
    
    for ind,dir_name in enumerate(dirs):
        t_text = "t: "+str(t_texts[ind])+"-"+str(t_texts[ind+1])+"GeV^2"
        dirname = dirbase + dir_name+"/"
        prelimplot.stitch_pics(dirname,save_dir="./tempouters/pics/",fig_name=dir_name,t_insert_text=t_text)
    
    #prelimplot.stitch_pics(dirname,save_dir="./pics/")


    #dirname = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/t_dependence_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/"
