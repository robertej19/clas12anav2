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
    datafile = fs["test_run_dir"]+fs["phi_fits_pkl_name"]
    data = data_getter.get_dataframe(datafile)

    plot_out_dirname = fs["test_run_dir"]
    dirname = fs['base_dir']+fs['output_dir']+fs["t_dep_dir"]+plot_out_dirname

    #dirname = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/t_dependence_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/"

    prelimplot.stitch_pics(dirname,save_dir="./")