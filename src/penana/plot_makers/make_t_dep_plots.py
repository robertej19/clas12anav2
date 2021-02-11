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

from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker
from src.penana.plot_makers import make_histos




def plot_t_dep(data,plot_out_dirname,xb_ranges,q2_ranges,ice_cream_enable):

    ic.disable()
    if ice_cream_enable:
        ic.enable()

    plot_out_dirpath = fs['base_dir']+fs['output_dir']+fs["t_dep_dir"]+plot_out_dirname
    file_maker.make_dir(plot_out_dirpath)

    for xb_ind in range(0,len(xb_ranges)-1):
        xBmax = xb_ranges[xb_ind+1]
        for q2_ind in range(0,len(q2_ranges)-1):
            Q2max = q2_ranges[q2_ind+1]
            ic(xBmax)
            ic(Q2max)
            data_t = data[(data['Q2max']==Q2max) & (data['xBmax']==xBmax)]
            #data_t = data[data['Q2max']==xBmax]

            x = data_t["tmax"]
            # y = data_t["A"]
            # z = data_t["B"]
            # w = data_t["C"]
            
            # y_err = data_t["A_uncert"]
            # z_err = data_t["B_uncert"]
            # w_err = data_t["C_uncert"]


            y = data_t["SigmaTeL"]
            z = data_t["SigmaTT"]
            w = data_t["SigmaLT"]
            
            y_err = data_t["SigmaTeL_uncert"]
            z_err = data_t["SigmaTT_uncert"]
            w_err = data_t["SigmaLT_uncert"]

            ic(y_err)
            #sys.exit()
            #A = T+L, B=TT, C=LT
            #A = black, B=blue, C=red
            fig, ax = plt.subplots()
            ax.errorbar(x,y,fmt='k',yerr=y_err,marker='o', ms=10,label="A - t+l")
            ax.errorbar(x,z,fmt='b',yerr=z_err,marker='o', ms=10,label="B - tt")
            ax.errorbar(x,w,fmt='r',yerr=w_err,marker='o', ms=10,label="C - lt")

            Q2maxstr = str(Q2max)
            if len(Q2maxstr) < 4:
                print("Q2maxstr is {} adding a 0 to yield: ".format(Q2maxstr))
                Q2maxstr = "0"+Q2maxstr
                print(Q2maxstr)
            #if len(Q2max) < 2:
            #    q2max = "0"+q2max

            t_title = 't-dependence-xb-{}-q2-{}'.format(xBmax,Q2maxstr)

            plt.title(t_title)
            plt.legend(loc='best')
            plt.xlabel(r't (GeV^2)')
            plt.ylabel(r'Unnormalized Scale')

            # plt.ylim(top=100) #ymax is your value
            # plt.ylim(bottom=-100) #ymin is your value

            
            plot_title = plot_out_dirpath + t_title+".png"
            plt.savefig(plot_title)
            plt.close()
            #rint("plot saved to {}".format(plot_title))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    args = parser.parse_args()

    fs = data_getter.get_json_fs()
    datafile = fs["test_run_dir"]+fs["phi_fits_pkl_name"]
    data = data_getter.get_dataframe(datafile)
    print(data)
    plot_out_dirname = fs["test_run_dir"]
    
    #xb_ranges = fs['xb_ranges_test']
    #q2_ranges = fs['q2_ranges_test']

    xb_ranges = fs['xb_ranges_clas6_14']
    q2_ranges = fs['q2_ranges_clas6_14']
    

    plot_t_dep(data,plot_out_dirname,xb_ranges,q2_ranges,args.v)

