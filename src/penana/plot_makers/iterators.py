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
from src.penana.fitting import phi_Fitter
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker
from src.utils import gamma_epsilon_calculator
from src.penana.plot_makers import make_histos


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

            make_histos.plot_2dhist(x_data,y_data,
                plotting_vars,plotting_ranges,colorbar=colorbar,plot_title=plot_title,
                saveplot=True,pics_dir=save_folder)


def iterate_3var(args,iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,plot_out_dir="pics/",t_pkl_dir="t_pkls/"):

    t_vals = []

    fs = data_getter.get_json_fs()
    data = data_getter.get_dataframe(datafile)
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs[iter_var_bins[0]] #t
    var2_bins = fs[iter_var_bins[1]] #xb
    var3_bins = fs[iter_var_bins[2]] #q2

    for ind,val in enumerate(var1_bins):
        if ind<10:
            ind = "0"+str(ind)
        print(val)
        file_maker.make_dir(plot_out_dir+"t"+str(ind)+"/")



    for var3_ind in range(1,len(var3_bins)):
        print("on {} index {}".format(iter_var_bins[2],var3_ind))
        var3_min = var3_bins[var3_ind-1]
        var3_max = var3_bins[var3_ind]
        for var2_ind in range(1,len(var2_bins)):
            print("on {} index {}".format(iter_var_bins[1],var2_ind))
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


                dir_ind = "0"+str(var1_ind-1) if (var1_ind-1)<10 else str(var1_ind-1)
                plot_out_dir_new = plot_out_dir + "t" + dir_ind+"/"

                

                fit_params, fit_cov, chisq, p = phi_Fitter.getPhiFit(x_data,plot_title,plot_out_dir_new,args)
                
                bb = bin_bounds

                if chisq == "nofit":
                    t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                            0,0,0,0,0,0,
                            0,0,0,0,0,0,0,
                            0,0,0])

                else:
                    A,B,C = fit_params[0],fit_params[1],fit_params[2]
                    a_err = np.sqrt(fit_cov[0][0])
                    b_err = np.sqrt(fit_cov[1][1])
                    c_err = np.sqrt(fit_cov[2][2])
                    
                    q2_mid = (bb[4]+bb[5])/2
                    xb_mid = (bb[2]+bb[3])/2
                    E = 10.6
                    Eprime = 3

                    Gamma, Epsilon = gamma_epsilon_calculator.calculate_gamma_epsilon(q2_mid,xb_mid,E,Eprime)

                    sigmaTeL = A/Gamma
                    sigmaTT = B/(Gamma*Epsilon)
                    sigmaLT = C/(Gamma*np.sqrt(2*Epsilon*(1+Epsilon)))

            
                    sigmaTeL_uncert = a_err/A*sigmaTeL 
                    sigmaTT_uncert = b_err/B*sigmaTT 
                    sigmaLT_uncert = c_err/C*sigmaLT 


                                    #xb,  #xb, #q2, q3,   t, t
                    t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                            A,B,C,a_err,b_err,c_err,
                            chisq,p,Gamma,Epsilon,sigmaTeL,sigmaTT,sigmaLT,
                            sigmaTeL_uncert,sigmaTT_uncert,sigmaLT_uncert])
                                
    df = pd.DataFrame(t_vals, columns=['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax',
                            'A','B','C','A_uncert','B_uncert','C_uncert','ChiSq','P',
                            'Gamma','Epsilon','SigmaTeL','SigmaTT','SigmaLT',
                            'SigmaTeL_uncert','SigmaTT_uncert','SigmaLT_uncert'])
    print("DF IS ----------")
    print(df)
    df.to_pickle(t_pkl_dir+fs["phi_fits_pkl_name"])



def iterate_3var_counts(args,iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,plot_out_dir="pics/",t_pkl_dir="t_pkls/"):

    t_vals = []

    fs = data_getter.get_json_fs()
    data = data_getter.get_dataframe(datafile)
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs[iter_var_bins[0]] #t
    var2_bins = fs[iter_var_bins[1]] #xb
    var3_bins = fs[iter_var_bins[2]] #q2

    for ind,val in enumerate(var1_bins):
        if ind<10:
            ind = "0"+str(ind)
        print(val)
        file_maker.make_dir(plot_out_dir+"t"+str(ind)+"/")



    for var3_ind in range(1,len(var3_bins)):
        print("on {} index {}".format(iter_var_bins[2],var3_ind))
        var3_min = var3_bins[var3_ind-1]
        var3_max = var3_bins[var3_ind]
        for var2_ind in range(1,len(var2_bins)):
            print("on {} index {}".format(iter_var_bins[1],var2_ind))
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

                
                dfq = query_maker.make_rev_query(iter_vars,bin_bounds)
                ic(dfq)
                data_filtered = data.query(dfq)   

                phi_bins = data_filtered["phi_min"].tolist()+[360,]
                bin_counts = data_filtered["counts"].tolist()
                #ic.enable()
                ic(data_filtered,phi_bins,bin_counts)  
                
                bbl = bin_bound_labels
                plot_title = '{}_fit_{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                dir_ind = "0"+str(var1_ind-1) if (var1_ind-1)<10 else str(var1_ind-1)
                plot_out_dir_new = plot_out_dir + "t" + dir_ind+"/"


                
                #ic.enable()
                #ic(plot_out_dir)
                fit_params, fit_cov, chisq, p = phi_Fitter.getPhiFit_prebinned(phi_bins,bin_counts,plot_title,plot_out_dir_new,args)
                

                bb = bin_bounds

                if chisq == "nofit":
                    t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                            0,0,0,0,0,0,
                            0,0,0,0,0,0,0,
                            0,0,0])

                else:
                    A,B,C = fit_params[0],fit_params[1],fit_params[2]
                    a_err = np.sqrt(fit_cov[0][0])
                    b_err = np.sqrt(fit_cov[1][1])
                    c_err = np.sqrt(fit_cov[2][2])
                    
                    q2_mid = (bb[4]+bb[5])/2
                    xb_mid = (bb[2]+bb[3])/2
                    E = 10.6
                    Eprime = 3

                    Gamma, Epsilon = gamma_epsilon_calculator.calculate_gamma_epsilon(q2_mid,xb_mid,E,Eprime)

                    sigmaTeL = A/Gamma
                    sigmaTT = B/(Gamma*Epsilon)
                    sigmaLT = C/(Gamma*np.sqrt(2*Epsilon*(1+Epsilon)))

            
                    sigmaTeL_uncert = a_err/A*sigmaTeL 
                    sigmaTT_uncert = b_err/B*sigmaTT 
                    sigmaLT_uncert = c_err/C*sigmaLT 


                                    #xb,  #xb, #q2, q3,   t, t
                    t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                            A,B,C,a_err,b_err,c_err,
                            chisq,p,Gamma,Epsilon,sigmaTeL,sigmaTT,sigmaLT,
                            sigmaTeL_uncert,sigmaTT_uncert,sigmaLT_uncert])
                                
    df = pd.DataFrame(t_vals, columns=['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax',
                            'A','B','C','A_uncert','B_uncert','C_uncert','ChiSq','P',
                            'Gamma','Epsilon','SigmaTeL','SigmaTT','SigmaLT',
                            'SigmaTeL_uncert','SigmaTT_uncert','SigmaLT_uncert'])
    print("DF IS ----------")
    print(df)
    df.to_pickle(t_pkl_dir+fs["phi_fits_pkl_name"])


def iterate_4var(args,iter_vars,iter_var_bins,
    datafile,t_pkl_dir="t_pkls/"):

    count_vals = []

    

    fs = data_getter.get_json_fs()
    data = data_getter.get_dataframe(datafile)
    #file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs[iter_var_bins[0]] #phi
    var2_bins = fs[iter_var_bins[1]] #t
    var3_bins = fs[iter_var_bins[2]] #xb
    var4_bins = fs[iter_var_bins[3]] #q2


    for var4_ind in range(1,len(var4_bins)):
        print("on {} index {}".format(iter_var_bins[3],var4_ind))
        var4_min = var4_bins[var4_ind-1]
        var4_max = var4_bins[var4_ind]
        for var3_ind in range(1,len(var3_bins)):
            print("on {} index {}".format(iter_var_bins[2],var3_ind))
            var3_min = var3_bins[var3_ind-1]
            var3_max = var3_bins[var3_ind]
            for var2_ind in range(1,len(var2_bins)):
                #print("on {} index {}".format(iter_var_bins[1],var2_ind))
                var2_min = var2_bins[var2_ind-1]
                var2_max = var2_bins[var2_ind]
                for var1_ind in range(1,len(var1_bins)):
                    var1_min = var1_bins[var1_ind-1]
                    var1_max = var1_bins[var1_ind]

                                    #phi    #phi      #t    #t         #xb      #xb      #q2     #q2
                    bin_bounds = [var1_min,var1_max,var2_min,var2_max,var3_min,var3_max,var4_min,var4_max]
                    bin_bound_labels = [str(bin_end) for bin_end in bin_bounds]
        
                    for ind,bin_end in enumerate(bin_bound_labels):
                        if bin_bounds[ind]<10 and bin_bounds[ind]>=1:
                            bin_bound_labels[ind] = "0"+bin_end


                    dfq = query_maker.make_query(iter_vars,bin_bounds)

                    data_filtered = data.query(dfq)       
                    num_events = len(data_filtered.index)

                    count_vals.append([var4_min,var4_max,var3_min,var3_max,var2_min,var2_max,var1_min,var1_max,num_events])


    df = pd.DataFrame(count_vals, columns=['Q2min','Q2max','xBmin', 'xBmax', 'tmin','tmax','phi_min','phi_max','counts'])
    print("DF IS ----------")
    #ic.enable()
    ic(df)
    df.to_pickle("pickled_counts.pkl")
                    
                    

if __name__ == "__main__":
    """
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
    iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
    plotting_ranges = [0,360,20]

    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    args = parser.parse_args()

    #set outdirs
    fs = data_getter.get_json_fs()

    datafile = "F18_Inbending_FD_SangbaekSkim_0_20210205/full_df_pickle-174_20210205_08-46-50.pkl"

    plot_out_dirname = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
    plot_out_dirpath = fs['base_dir']+fs['output_dir']+fs["phi_dep_dir"]+plot_out_dirname
    t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+plot_out_dirname

    
    iterate_3var(args,iter_vars,plotting_vars,iter_var_bins,
        datafile,plotting_ranges,plot_out_dir=plot_out_dirpath,t_pkl_dir=t_pkl_dirpath)
    """
    """
    #############################
    #Test iterate_4var
    iter_vars = ['phi','t','xb','q2'] 
    #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
    iter_var_bins = ["phi_ranges_clas6_14","t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]

    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    args = parser.parse_args()

    #set outdirs
    fs = data_getter.get_json_fs()

    datafile ="lund_processed_pickles/testlund.txt.pkl"

    plot_out_dirname = "lund_processed_pickles/"
    t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+plot_out_dirname

    
    iterate_4var(args,iter_vars,iter_var_bins,
        datafile,t_pkl_dir=t_pkl_dirpath)
    """
     #############################
    #Test iterate_3var_counts
    iter_vars = ['tmin','xBmin','Q2min']
    plotting_vars = ['phi']
    #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
    iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
    plotting_ranges = [0,360,20]

    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    args = parser.parse_args()

    #set outdirs
    fs = data_getter.get_json_fs()

    datafile = "pickled_counts/pickled_counts_test.pkl"

    plot_out_dirname = "test_pickler/"
    plot_out_dirpath = fs['base_dir']+fs['output_dir']+fs["phi_dep_dir"]+plot_out_dirname
    t_pkl_dirpath = fs['base_dir']+fs['data_dir']+fs["pandas_dir"]+plot_out_dirname

    
    iterate_3var_counts(args,iter_vars,plotting_vars,iter_var_bins,
        datafile,plotting_ranges,plot_out_dir=plot_out_dirpath,t_pkl_dir=t_pkl_dirpath)