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
import time
import sys
import subprocess
import os
import json
from datetime import datetime
import shutil

#This project
from src.utils import filestruct
from src.utils import query_maker
from src.utils import file_maker
from src.utils import iterators
from src.data_processing_formatting.hipo_root_cuts.dvep_cutter import root_batch_dvpip_cutter
from src.data_processing_formatting.root_processor import root_to_txt
from src.data_processing_formatting.root_processor import txt_to_pandas


from src.data_analysis_plotting.plot_makers import make_t_dep_plots

from src.data_analysis_plotting.plot_makers import make_histos
from src.data_analysis_plotting.picture_tools import prelimplot

#This is for viewing ROOT file information. The steps are:
# 1 Apply DVEP cuts to Root files
# 2 RIP root with uproot!
# 3 Convert to Pandas
# 4 Iterate the day away

###
#Function defs
###


now = datetime.now()
dt_string = now.strftime("%Y%m%d-%H-%M")

##################################################################
##################################################################
##################################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Args.')
    parser.add_argument('-v', help='enables ice cream output',default=False,action="store_true")
    parser.add_argument('-s','--start', type=int, help='hop in point of program',default=1)
    parser.add_argument('-p','--stop', type=int,help='hop out point of program',default=10)
    parser.add_argument('-l','--lumi', type=int,help='calculate lumi',default=10)
    parser.add_argument('-i','--hist1',help='make q2 vs xb graph',default=False,action="store_true")
    args = parser.parse_args()

    fs = filestruct.fs()
    dir_to_process = fs.data_basename 
    outputs_dir = fs.base_dir+fs.output_dir 

    base_root_dir = fs.base_dir+fs.data_dir+fs.data_2_dir+dir_to_process
    output_DVEP_dir = fs.base_dir+fs.data_dir+fs.data_3_dir+dir_to_process
    output_root_txt_dir = fs.base_dir + fs.data_dir+fs.data_4_dir+dir_to_process 
    output_root_pandas_dir = fs.base_dir + fs.data_dir+fs.pandas_dir+dir_to_process 
    whole_data_pkl_name = fs.whole_data_pkl_name

    counted_data_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + dir_to_process
    counted_pickled_out_name = fs.counted_pickled_out_name

    counted_lund_pandas_dir = fs.base_dir + fs.data_dir + fs.lund_dir + fs.binned_lund_pandas+fs.lund_test_run

    counted_data_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + dir_to_process
    uncounted_real_data_pandas = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.test_run_dir + fs.real_dataset_full_pandas

    #print(args)
    #sys.exit()

    if args.v:
        ic.enable()

    if args.start <=1 and args.stop >=1:
        root_macro = fs.base_dir+fs.src_dir+fs.data_processing_formatting + fs.dvep_cut_dir+fs.root_macro_script

        root_batch_dvpip_cutter.process_root_files(root_macro,base_root_dir+dir_to_process,output_DVEP_dir) 
        print("Stage 1 complete")

    if args.start <=2 and args.stop >=2:
        root_to_txt.root_to_txt(output_DVEP_dir,output_root_txt_dir)

        print("Stage 2 complete")
    
    if args.start <=3 and args.stop >=3:
        txt_to_pandas.txt_to_pandas(output_root_txt_dir,output_root_pandas_dir,whole_data_pkl_name)
        print("Stage 3 complete")

    if args.start <=4 and args.stop >=4:

        iter_vars = ['phi','t','xb','q2'] 
        iter_var_bins = ["phi_ranges_clas6_14","t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]

        df = pd.read_pickle(output_root_pandas_dir+whole_data_pkl_name)

        #Gamma, Epsilon = gamma_epsilon_calculator.calculate_gamma_epsilon(q2_mid,xb_mid,E,Eprime)


        alpha = 1/137 #Fund const
        mP = 0.938 #Mass proton
        prefix = alpha/(8*np.pi)
        E = 10.6

        epsilon = 0.5

        ic.enable()
        df['y'] = (E-df['Nu'])/E
        df['q24E2'] = df['q2']/(4*E*E)
        df['epsi'] = (1-df['y']-df['q24E2'])/(1-df['y']+(df['q24E2']**2)/2+df['q24E2'])

        df['gamma'] = prefix*df['q2']/(mP*mP*E*E)*(1-df['xb'])/(df['xb']**3)*(1/(1-df['epsi']))/(2*np.pi)
        ic(df)
        ic(df['gamma'].min())
        ic(df['gamma'].max())
        


        

        iterators.iterate_4var(args,iter_vars,iter_var_bins,
            df,t_pkl_dir=counted_data_pandas_dir,pkl_filename=counted_pickled_out_name)
        
        print("Stage 4 complete")

    if args.start <=5 and args.stop >=5:


        # counted_real_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.test_run_dir
    
        # dataframe_real = pd.read_pickle(counted_real_pandas_dir+counted_pickled_out_name)
        # dataframe1 = dataframe_real

        #dataframe1 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        dataframe1 = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/data/5_pickled_pandas/F18_Inbending_FD_SangbaekSkim_0_20210205/counted_4D_out.pkl")
        
        
        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts
        iter_vars = ['tmin','xBmin','Q2min']
        plotting_vars = ['phi']
        #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
        iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
        plotting_ranges = [0,360,20]


        iterators.iterate_3var_counts_single(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,
            plot_out_dir=outputs_dir + fs.phi_dep_dir+dir_to_process+"corrected/",dataframe=dataframe1)
        print("Stage 5 complete")



    if args.start <=6 and args.stop >=6:

        #output/phi_1d_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/acceptance/
        input_dir = outputs_dir + fs.phi_dep_dir+dir_to_process+"acceptance/"
        output_dir = outputs_dir+fs.data_outs+dir_to_process
        file_maker.make_dir(output_dir+"acceptance/")
        
        t_texts = fs.t_ranges_clas6_14
        t_dirs = ["t00","t01","t02","t03","t04","t05","t06","t07","t08","t09","t10","t11","t12"]
        xb_ranges = fs.xb_ranges_clas6_14
        q2_ranges = fs.q2_ranges_clas6_14
        
        for ind,input_dirname in enumerate(t_dirs):
            t_text = "t: "+str(t_texts[ind])+"-"+str(t_texts[ind+1])+"GeV^2"
            #outdir = output_dir
            #file_maker.make_dir(output_dir)
            prelimplot.stitch_pics(input_dir+input_dirname+"/",xb_ranges,q2_ranges,save_dir= output_dir+"acceptance/",fig_name=input_dirname,t_insert_text=t_text)

        print("Stage 6 complete")

    if args.start <=7 and args.stop >=7:

        print(counted_data_pandas_dir+counted_pickled_out_name)
        print(counted_lund_pandas_dir+counted_pickled_out_name)

        #sys.exit()

        #dataframe0 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        #dataframe1 = pd.read_pickle(counted_lund_pandas_dir+counted_pickled_out_name)

        corrected_df = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/data/5_pickled_pandas/F18_Inbending_FD_SangbaekSkim_0_20210205/counted/counted_4D_out.pkl")
        raw_df = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/data/5_pickled_pandas/F18_Inbending_FD_SangbaekSkim_0_20210205/counted_4D_out.pkl")
        
        dataframe0 = raw_df
        dataframe1 = corrected_df
        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts
        iter_vars = ['tmin','xBmin','Q2min']
        plotting_vars = ['phi']
        #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
        iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
        plotting_ranges = [0,360,20]


        iterators.iterate_3var_counts_double(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,
            plot_out_dir=outputs_dir + fs.phi_dep_dir+dir_to_process+"acceptance/",dataframe0=dataframe0,dataframe1=dataframe1)
        print("Stage 7 complete")

    if args.start <=8 and args.stop >=8:

        print(counted_data_pandas_dir+counted_pickled_out_name)
        print(counted_lund_pandas_dir+counted_pickled_out_name)

        ic.enable()
        
        # df_real = pd.read_pickle(uncounted_real_data_pandas)
        # ic(df_real)


        # iter_vars = ['phi','t','xb','q2'] 
        # iter_var_bins = ["phi_ranges_clas6_14","t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]

        counted_sim_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + "testpi01Ksim/"
    
        # iterators.iterate_4var(args,iter_vars,iter_var_bins,
        #     df_real,t_pkl_dir=counted_real_pandas_dir,pkl_filename=counted_pickled_out_name)
        # sys.exit()

        dataframe_sim = pd.read_pickle(counted_sim_pandas_dir+counted_pickled_out_name)
        dataframe_real = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        dataframe_lund = pd.read_pickle(counted_lund_pandas_dir+counted_pickled_out_name)

    

        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts
        iter_vars = ['phi_min','tmin','xBmin','Q2min'] 
        iter_var_bins = ["phi_ranges_clas6_14","t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]

        #Q2min  Q2max  xBmin  xBmax  tmin   tmax  phi_min  phi_max  counts


        iterators.iterate_4var_acc_maker(args,iter_vars,iter_var_bins,
            dataframe_sim,dataframe_lund,dataframe_real,t_pkl_dir=counted_data_pandas_dir+"counted/",pkl_filename=counted_pickled_out_name)
        print("Stage 8 complete")

    if args.start <=9 and args.stop >=9:


        # counted_real_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.test_run_dir
    
        # dataframe_real = pd.read_pickle(counted_real_pandas_dir+counted_pickled_out_name)
        # dataframe1 = dataframe_real

        #dataframe1 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        dataframe1 = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/data/5_pickled_pandas/F18_Inbending_FD_SangbaekSkim_0_20210205/counted/counted_4D_out.pkl")
        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts
        ic.enable()
        ic(dataframe1)

        sys.exit()

        iter_vars = ['tmin','xBmin','Q2min']
        plotting_vars = ['phi']
        #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
        iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
        plotting_ranges = [0,360,20]


        iterators.iterate_3var_counts_single_with_t(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,
            plot_out_dir=outputs_dir + fs.phi_dep_dir+dir_to_process+"corrected/",dataframe=dataframe1)
        print("Stage 5 complete")

    if args.lumi == 14:
        print("we here")

        # counted_real_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.test_run_dir
    
        # dataframe_real = pd.read_pickle(counted_real_pandas_dir+counted_pickled_out_name)
        # dataframe1 = dataframe_real

        #dataframe1 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        dataframe1 = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/data/5_pickled_pandas/F18_Inbending_FD_SangbaekSkim_0_20210205/full_dataset_pickle.pkl")
        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts
        ic.enable()
        ic(dataframe1)

        #df1 = dataframe1.query("run == 5032")
        run_numbers = dataframe1.run.unique()

        ibcs = []
        for run_num in run_numbers:
            print("on run num {}".format(run_num))
            df00 = dataframe1.query("run == {}".format(run_num))
            int_beam_charge = df00["luminosity"].max() - df00["luminosity"].min()
            ibcs.append(int_beam_charge)

        df001 = dataframe1.query("run == {}".format(5032))
        int_beam_charge_5032 = df001["luminosity"].max() - df001["luminosity"].min()
        

        

        def lumi(beam_q):
            #Beam charge comes in units of nC, so needs a factor of
            # 1e-9 to convert to C
            constant = 1e-9
            N_a = 6e23
            e_charge = 1.6e-19
            target_len = 5 #cm
            target_den = 0.07 #g/cm^3

            lumi = constant*N_a*target_len*target_den*beam_q/e_charge

            return(lumi)

        print(ibcs)

        total_beam_charge = sum(ibcs)

        print(total_beam_charge)

        testarr = [1,2,3]
        print(sum(testarr))

        ic.enable()
        ic(int_beam_charge_5032)
        ic(lumi(int_beam_charge_5032))
        ic(lumi(total_beam_charge))

        sys.exit()

        iter_vars = ['tmin','xBmin','Q2min']
        plotting_vars = ['phi']
        #iter_var_bins = ["t_ranges_test","xb_ranges_test","q2_ranges_test"]
        iter_var_bins = ["t_ranges_clas6_14","xb_ranges_clas6_14","q2_ranges_clas6_14"]
        plotting_ranges = [0,360,20]


        iterators.iterate_3var_counts_single_with_t(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,
            plot_out_dir=outputs_dir + fs.phi_dep_dir+dir_to_process+"corrected/",dataframe=dataframe1)
        print("Stage 5 complete")

    

    if args.lumi == 15:
        print("we here")

        # counted_real_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.test_run_dir
    
        # dataframe_real = pd.read_pickle(counted_real_pandas_dir+counted_pickled_out_name)
        # dataframe1 = dataframe_real

        #dataframe1 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        dataframe1 = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/t_pkls/phi_fit_vals_14_corrected.pkl")
        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts
        ic.enable()
        ic(dataframe1)
        sys.exit()

        plot_out_dirname = "acceptance_corrected/"
        xb_ranges = fs.xb_ranges_clas6_14
        q2_ranges = fs.q2_ranges_clas6_14


        make_t_dep_plots.plot_t_dep(dataframe1,plot_out_dirname,xb_ranges,q2_ranges,args.v)

    if args.lumi == 151:
        print("we here")

        #output/phi_1d_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/acceptance/
        input_dir = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/t_dependence_hists/acceptance_corrected/"
        output_dir = outputs_dir+fs.data_outs+dir_to_process
        file_maker.make_dir(output_dir+"acceptance_corrected/")
        
        xb_ranges = fs.xb_ranges_clas6_14
        q2_ranges = fs.q2_ranges_clas6_14
        
        
        prelimplot.stitch_pics(input_dir,xb_ranges,q2_ranges,save_dir= output_dir+"acceptance_corrected/")

    if args.lumi == 515:
        print("we here")

        clas6_data = pd.read_csv("raw-clas6-data.csv")
        ic.enable()

        # counted_real_pandas_dir = fs.base_dir + fs.data_dir + fs.pandas_dir + fs.test_run_dir
    
        # dataframe_real = pd.read_pickle(counted_real_pandas_dir+counted_pickled_out_name)
        # dataframe1 = dataframe_real

        #dataframe1 = pd.read_pickle(counted_data_pandas_dir+counted_pickled_out_name)
        dataframe1 = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/t_pkls/phi_fit_vals_14_corrected.pkl")
        ### 4 - Plotting: Plot either 2,3, or 4 dimensionally  ---- ###
        #Test iterate_3var_counts

        gamma_ep_df = pd.read_pickle("/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/data/5_pickled_pandas/F18_Inbending_FD_SangbaekSkim_0_20210205/gamma_ep_counted_4D_out.pkl")
        
        ic.enable()
        ic(dataframe1)
        ic(gamma_ep_df)


        plot_out_dirname = "acceptance_corrected/"
        xb_ranges = fs.xb_ranges_clas6_14
        q2_ranges = fs.q2_ranges_clas6_14


        make_t_dep_plots.plot_t_dep_with_clas(dataframe1,clas6_data,plot_out_dirname,xb_ranges,q2_ranges,args.v,g_ep_df=gamma_ep_df)
