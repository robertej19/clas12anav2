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




def txt_to_pandas(data_dir,output_dir,output_pkl_name):

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

    output_filename = output_pkl_name

    data.to_pickle(output_dir+output_filename)
    print("Saved file at {}".format(output_dir+output_filename))

    return output_filename

if __name__ == "__main__":
    fs = filestruct.fs()

    data_dir = fs.base_dir + fs.data_dir+fs.data_4_dir+fs.data_basename 
    output_dir = fs.base_dir + fs.data_dir+fs.pandas_dir+fs.data_basename
    whole_data_pkl_name = fs.whole_data_pkl_name

    txt_to_pandas(data_dir,output_dir,whole_data_pkl_name)
    