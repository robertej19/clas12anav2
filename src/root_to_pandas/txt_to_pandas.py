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

#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker
from src.penana.plot_makers import plot_maker_hist_plotter



fs = data_getter.get_json_fs()


#FD
#datafile_dir = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
#data_out_dir = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
#CD
datafile_dir = "F18_Inbending_CD_SangbaekSkim_0_20210205/"
data_out_dir = "F18_Inbending_CD_SangbaekSkim_0_20210205/"

data_dir = fs['base_dir']+fs['data_dir']+fs["data_4_dir"]+datafile_dir
data_list = os.listdir(data_dir)

output_dir = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+data_out_dir
file_maker.make_dir(output_dir)


data = pd.DataFrame()
        
for datacount, ijk in enumerate(data_list):
    ic(datacount)
    print(ijk)
    frame = pd.read_csv(data_dir+ijk, sep=",", header=0)
    data = data.append(frame)

#data = pd.read_csv('afterfixes.txt', sep=",", header=None)
#data.columns = ["run_num", "event_num", "num_in_fd", "num_in_cd","helicity","xB","Q2","t","Phi"]

#data.columns = ["run_num", "event_num", "num_in_fd", "num_in_cd","helicity","xB","Q2","t","Phi","W","ThetaXPi","Diff_pX","Diff_pY","MM_EPX2","ME_EPGG","Pi_Mass"]
#data.columns = ["Q2","xB","t","Phi"]


ic(data.shape)

column_titles = list(data)
ic(column_titles)

timestamp = pd.Timestamp("now").strftime('%Y%m%d_%H-%M-%S')
ic(timestamp)


output_filename = "full_df_pickle-{}_{}.pkl".format(len(data_list),timestamp)

data.to_pickle(output_dir+output_filename)
print("Saved file at {}".format(output_dir+output_filename))