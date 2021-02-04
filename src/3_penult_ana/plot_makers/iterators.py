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
from utils import data_getter
from utils import query_maker
from plot_makers import plot_maker_hist2d_plotter




fs = data_getter.get_json_fs()

xb_ranges = fs["xb_ranges_test"]
q2_ranges = fs["q2_ranges_test"]

print(len(xb_ranges))
print(len(q2_ranges))

variables = ['xB','Q2']
datafile = "F18In_168_20210129/skims-168.pkl"
plotting_ranges = [0,15,100,0,300,120]


for q2_ind in range(1,len(q2_ranges)):
    q2_min = q2_ranges[q2_ind-1]
    q2_max = q2_ranges[q2_ind]
    for xb_ind in range(1,len(xb_ranges)):
        xb_min = xb_ranges[xb_ind-1]
        xb_max = xb_ranges[xb_ind]
        print(xb_min,xb_max,q2_min,q2_max)
        ranges = [xb_min,xb_max,q2_min,q2_max]

        dfq = query_maker.make_query(variables,ranges)

        plot_maker_hist2d_plotter.plot_2dhist(datafile,variables,plotting_ranges,
            dataframe_query=dfq)
        