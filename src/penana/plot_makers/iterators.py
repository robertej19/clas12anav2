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
from fitting import phi_Fitter
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
                if bin_bounds[ind]<10 and bin_bounds[ind]>=1:
                    bin_bound_labels[ind] = "0"+bin_end


            dfq = query_maker.make_query(iter_vars,bin_bounds)

            data_filtered = data.query(dfq)           
            x_data = data_filtered[plotting_vars[0]]
            y_data = data_filtered[plotting_vars[1]]

            ic(iter_vars,bin_bound_labels)
            bbl = bin_bound_labels
            plot_title = '{}_vs_{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],plotting_vars[1],
                iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3])
            ic(plot_title)

            plot_maker_hist_plotter.plot_2dhist(x_data,y_data,
                plotting_vars,plotting_ranges,colorbar=colorbar,plot_title=plot_title,
                saveplot=True,pics_dir=save_folder)


def iterate_3var(iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,plot_out_dir="pics/",t_pkl_dir="t_pkls/"):

    t_vals = []

    fs = data_getter.get_json_fs()
    data = data_getter.get_dataframe(datafile)
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs[iter_var_bins[0]] #t
    var2_bins = fs[iter_var_bins[1]] #xb
    var3_bins = fs[iter_var_bins[2]] #q2

    for var3_ind in range(1,len(var3_bins)):
        print("on third index {}".format(var3_ind))
        var3_min = var3_bins[var3_ind-1]
        var3_max = var3_bins[var3_ind]
        for var2_ind in range(1,len(var2_bins)):
            print("on second index {}".format(var2_ind))
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

                x_data = data_filtered[plotting_vars[0]]

                bbl = bin_bound_labels
                plot_title = '{}_fit_{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                fit_params = phi_Fitter.getPhiFit(x_data,plot_title,plot_out_dir)

                bb = bin_bounds
                t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],fit_params[0],fit_params[1],fit_params[2]])
                                #xb,  #xb, #q2, q3,   t, t
    df = pd.DataFrame(t_vals, columns=['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax','A','B','C'])
    print("DF IS ----------")
    print(df)
    df.to_pickle(t_pkl_dir+"/phi_fit_vals.pkl")


if __name__ == "__main__":
    
    #Path after 5_pickled_pandas/
    #datafile = "F18In_168_20210129/skims-168.pkl"
    datafile = "F18_Inbending_FD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-46-50.pkl"
    #datafile = "F18_Inbending_CD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-54-11.pkl"

    #Test iterate_2var
    
    iter_var_bins = ["xb_ranges_clas6","q2_ranges_clas6"]

    plotting_ranges = [0,360,36,0,6,20]
    
    #iterate_2var(iter_vars,plotting_vars,iter_var_bins,
    #    datafile,plotting_ranges,colorbar=False)
    
    #######################################################

    #Test iterate_3var
    iter_vars = ['t','xb','q2']
    plotting_vars = ['phi']
    #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
    iter_var_bins = ["t_ranges_clas6","xb_ranges_clas6","q2_ranges_clas6"]
    plotting_ranges = [0,360,20]

    #set outdirs
    fs = data_getter.get_json_fs()

    datafile = "F18_Inbending_FD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-46-50.pkl"

    plot_out_dirname = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
    plot_out_dirpath = fs['base_dir']+fs['output_dir']+fs["phi_dep_dir"]+plot_out_dirname
    t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+plot_out_dirname

    
    iterate_3var(iter_vars,plotting_vars,iter_var_bins,
        datafile,plotting_ranges,plot_out_dir=plot_out_dirpath,t_pkl_dir=t_pkl_dirpath)
