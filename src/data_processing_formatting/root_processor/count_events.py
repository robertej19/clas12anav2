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


datafile ="lund_processed_pickles/testlund.txt.pkl"
df = data_getter.get_dataframe(datafile)
ic(df)

fs = data_getter.get_json_fs()
xb_r = fs["xb_ranges_clas6_14"]
q2b_r = fs["q2_ranges_clas6_14"]
t_r = fs["t_ranges_clas6_14"]
phi_r = fs["phi_ranges_clas6_14"]


var1_bins = fs[iter_var_bins[0]] #t
var2_bins = fs[iter_var_bins[1]] #xb
var3_bins = fs[iter_var_bins[2]] #q2


for var4_ind in range(1,len(var4_bins)):
        #print("on {} index {}".format(iter_var_bins[2],var3_ind))
        var4_min = var4_bins[var4_ind-1]
        var4_max = var4_bins[var4_ind]
    for var3_ind in range(1,len(var3_bins)):
        #print("on {} index {}".format(iter_var_bins[2],var3_ind))
        var3_min = var3_bins[var3_ind-1]
        var3_max = var3_bins[var3_ind]
        for var2_ind in range(1,len(var2_bins)):
            #print("on {} index {}".format(iter_var_bins[1],var2_ind))
            var2_min = var2_bins[var2_ind-1]
            var2_max = var2_bins[var2_ind]
            for var1_ind in range(1,len(var1_bins)):
                var1_min = var1_bins[var1_ind-1]
                var1_max = var1_bins[var1_ind]

                                #t    #t         #xb      #xb      #q2     #q2
                bin_bounds = [var1_min,var1_max,var2_min,var2_max,var3_min,var3_max]
                bin_bound_labels = [str(bin_end) for bin_end in bin_bounds]
    
                for ind,bin_end in enumerate(bin_bound_labels):
                    if bin_bounds[ind]<10 and bin_bounds[ind]>=1:
                        bin_bound_labels[ind] = "0"+bin_end


                dfq = query_maker.make_query(iter_vars,bin_bounds)

                data_filtered = data.query(dfq) 

"""
out_labels = ["run","event","luminosity","helicity","Ebeam","Eprime","q2","xb","t","phi"]

def process_lunds_into_events(df):
    events_list = []
    num_events = df["event_num"].max()
    ic(num_events)
    for ind in range(0,num_events+1):
        if ind % 1000 ==0:
            ic.enable()


binner_labels = ["q2","xb","t","phi","counts"]




df_out = pd.DataFrame(events_list, columns=out_labels)
ic(df_out)
df_out.to_pickle("counted_bins.pkl")
"""