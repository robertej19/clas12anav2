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
from utils import file_maker
from plot_makers import plot_maker_hist_plotter


def iterate_2var(iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,colorbar=True,save_folder="pics/"):

    fs = data_getter.get_json_fs()
    data = data_getter.get_dataframe(datafile)
    file_maker.make_dir(save_folder)
    
    var1_bins = fs[iter_var_bins[0]]
    var2_bins = fs[iter_var_bins[1]]

    for var2_ind in range(1,len(var2_bins)):
        var2_min = var2_bins[var2_ind-1]
        var2_max = var2_bins[var2_ind]
        for var1_ind in range(1,len(var1_bins)):
            var1_min = var1_bins[var1_ind-1]
            var1_max = var1_bins[var1_ind]

            bin_bounds = [var1_min,var1_max,var2_min,var2_max]
            bin_bound_labels = [str(bin_end) for bin_end in bin_bounds]
            for ind,bin_end in enumerate(bin_bound_labels):
                if len(bin_end)<2:
                    bin_bound_labels[ind] = "0"+bin_end


            dfq = query_maker.make_query(iter_vars,bin_bounds)

            data_filtered = data.query(dfq)           
            x_data = data_filtered[plotting_vars[0]]
            y_data = data_filtered[plotting_vars[1]]

            ic(iter_vars,bin_bound_labels)
            bbl = bin_bound_labels
            plot_title = '{}_vs_{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],plotting_vars[1],
                iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3])


            plot_maker_hist_plotter.plot_2dhist(x_data,y_data,
                plotting_vars,plotting_ranges,colorbar=colorbar,plot_title=plot_title,
                saveplot=True,pics_dir=save_folder)


def iterate_3var(iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,save_folder="pics/"):

    fs = data_getter.get_json_fs()
    data = data_getter.get_dataframe(datafile)
    file_maker.make_dir(save_folder)
    
    var1_bins = fs[iter_var_bins[0]]
    var2_bins = fs[iter_var_bins[1]]
    var3_bins = fs[iter_var_bins[2]]

    for var3_ind in range(1,len(var3_bins)):
        var3_min = var3_bins[var3_ind-1]
        var3_max = var3_bins[var3_ind]
        for var2_ind in range(1,len(var2_bins)):
            var2_min = var2_bins[var2_ind-1]
            var2_max = var2_bins[var2_ind]
            for var1_ind in range(1,len(var1_bins)):
                var1_min = var1_bins[var1_ind-1]
                var1_max = var1_bins[var1_ind]


                bin_bounds = [var1_min,var1_max,var2_min,var2_max,var3_min,var3_max]
                bin_bound_labels = [str(bin_end) for bin_end in bin_bounds]
                for ind,bin_end in enumerate(bin_bound_labels):
                    if len(bin_end)<2:
                        bin_bound_labels[ind] = "0"+bin_end


                dfq = query_maker.make_query(iter_vars,bin_bounds)

                data_filtered = data.query(dfq)           
                x_data = data_filtered[plotting_vars[0]]

                ic(iter_vars,bin_bound_labels)
                bbl = bin_bound_labels
                plot_title = '{}__{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                plot_maker_hist_plotter.plot_1dhist(x_data,
                    plotting_vars,plotting_ranges,plot_title=plot_title,
                    saveplot=True,pics_dir=save_folder)


if __name__ == "__main__":
    
    datafile = "F18In_168_20210129/skims-168.pkl"
    
    #Test iterate_2var
    iter_vars = ['xB','Q2']
    plotting_vars = ['Phi','t']
    iter_var_bins = ["xb_ranges_clas6","q2_ranges_clas6"]

    plotting_ranges = [0,360,20,0,6,10]
    
    iterate_2var(iter_vars,plotting_vars,iter_var_bins,
        datafile,plotting_ranges,colorbar=False)
    
    #Test iterate_3var
    iter_vars = ['xB','Q2','t']
    plotting_vars = ['Phi']
    #iter_var_bins = ["xb_ranges_test","q2_ranges_test","t_ranges_test"]
    iter_var_bins = ["xb_ranges_clas6","q2_ranges_clas6","t_ranges_clas6"]

    plotting_ranges = [0,360,20]
    
    #iterate_3var(iter_vars,plotting_vars,iter_var_bins,
    #    datafile,plotting_ranges)
