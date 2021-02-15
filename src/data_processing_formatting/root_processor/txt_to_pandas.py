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
from src.utils import filestruct
from src.utils import query_maker
from src.utils import file_maker




def txt_to_pandas(data_dir,output_dir):

    data_list = os.listdir(data_dir)
    file_maker.make_dir(output_dir)


    data = pd.DataFrame()
            
    for datacount, ijk in enumerate(data_list):
        ic(datacount)
        print(ijk)
        frame = pd.read_csv(data_dir+ijk, sep=",", header=0)
        data = data.append(frame)


    ic(data.shape)

    column_titles = list(data)
    ic(column_titles)

    timestamp = pd.Timestamp("now").strftime('%Y%m%d_%H-%M-%S')
    ic(timestamp)

    output_filename = "full_df_pickle-{}_{}.pkl".format(len(data_list),timestamp)

    data.to_pickle(output_dir+output_filename)
    print("Saved file at {}".format(output_dir+output_filename))

if __name__ == "__main__":
    fs = filestruct.fs()

    data_dir = fs.base_dir + fs.data_dir+fs.data_4_dir+fs.data_basename 
    output_dir = fs.base_dir + fs.data_dir+fs.pandas_dir+fs.data_basename 

    txt_to_pandas(data_dir,output_dir)
    