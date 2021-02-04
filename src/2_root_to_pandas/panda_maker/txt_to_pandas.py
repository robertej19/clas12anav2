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




#data_dir = "plottingfiles/"
#data_dir = "../rooty/plottingfiles/"
#data_dir = "groovy-test/"
#data_dir = "../rooty/op_dir/final_txts/"
data_dir = "./"
#data_lists = os.listdir(data_dir)
data_lists = ["output_root_file.txt"]

data = pd.DataFrame()

        
for datacount, ijk in enumerate(data_lists):
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

output_dir = "pickled_pandas/"
if not os.path.isdir(output_dir):
	print('creating output directory {}'.format(output_dir))
	subprocess.call(['mkdir','-p',output_dir])


output_filename = "skims-{}_{}.pkl".format(len(data_lists),timestamp)

data.to_pickle(output_dir+output_filename)
print("Saved file at {}".format(output_dir+output_filename))