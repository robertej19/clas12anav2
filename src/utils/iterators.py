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

#This project
from src.utils import filestruct
from src.utils import query_maker
from src.utils import file_maker
from src.utils import gamma_epsilon_calculator
from src.data_analysis_plotting.plot_makers import make_histos
from src.data_analysis_plotting.fitting import phi_Fitter


def iterate_2var(iter_vars,plotting_vars,iter_var_bins,
    datafile,plotting_ranges,colorbar=True,save_folder="pics/"):

    fs = filestruct.fs()
    data = pd.read_pickle(datafile)
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

    fs = filestruct.fs()
    data = pd.read_pickle(datafile)
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


def iterate_3var_counts_single(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,plot_out_dir,dataframe):

    t_vals = []

    data = dataframe
    
    fs = filestruct.fs()
    
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs.__getattribute__(iter_var_bins[0]) #t
    var2_bins = fs.__getattribute__(iter_var_bins[1]) #xb
    var3_bins = fs.__getattribute__(iter_var_bins[2]) #q2



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
                data_filtered = data.query(dfq)[1:]   

                ic(data_filtered)
                #sys.exit()

                phi_bins = data_filtered["phi_min"].tolist()#+[360,]
                bin_counts_0 = data_filtered["counts_corrected"].tolist()
                
                ic.disable()
                ic(bin_counts_0)
                ic(phi_bins)
                ##ic.enable()
                
                bbl = bin_bound_labels
                plot_title = '{}_fit_{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                dir_ind = "0"+str(var1_ind-1) if (var1_ind-1)<10 else str(var1_ind-1)
                plot_out_dir_new = plot_out_dir + "t" + dir_ind+"/"


                
                ##ic.enable()
                #ic(plot_out_dir)
                #fit_params, fit_cov, chisq, p = phi_Fitter.getPhiFit_prebinned(phi_bins,bin_counts,plot_title,plot_out_dir_new,args)
                
                phi_Fitter.plotPhi_single(phi_bins,bin_counts_0,plot_title,plot_out_dir_new,args)

                # bb = bin_bounds

                # if chisq == "nofit":
                #     t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                #             0,0,0,0,0,0,
                #             0,0,0,0,0,0,0,
                #             0,0,0])

                # else:
                #     A,B,C = fit_params[0],fit_params[1],fit_params[2]
                #     a_err = np.sqrt(fit_cov[0][0])
                #     b_err = np.sqrt(fit_cov[1][1])
                #     c_err = np.sqrt(fit_cov[2][2])
                    
                #     q2_mid = (bb[4]+bb[5])/2
                #     xb_mid = (bb[2]+bb[3])/2
                #     E = 10.6
                #     Eprime = 3

                #     Gamma, Epsilon = gamma_epsilon_calculator.calculate_gamma_epsilon(q2_mid,xb_mid,E,Eprime)

                #     sigmaTeL = A/Gamma
                #     sigmaTT = B/(Gamma*Epsilon)
                #     sigmaLT = C/(Gamma*np.sqrt(2*Epsilon*(1+Epsilon)))

            
                #     sigmaTeL_uncert = a_err/A*sigmaTeL 
                #     sigmaTT_uncert = b_err/B*sigmaTT 
                #     sigmaLT_uncert = c_err/C*sigmaLT 


                #                     #xb,  #xb, #q2, q3,   t, t
                #     t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                #             A,B,C,a_err,b_err,c_err,
                #             chisq,p,Gamma,Epsilon,sigmaTeL,sigmaTT,sigmaLT,
                #             sigmaTeL_uncert,sigmaTT_uncert,sigmaLT_uncert])
                                
    # df = pd.DataFrame(t_vals, columns=['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax',
    #                         'A','B','C','A_uncert','B_uncert','C_uncert','ChiSq','P',
    #                         'Gamma','Epsilon','SigmaTeL','SigmaTT','SigmaLT',
    #                         'SigmaTeL_uncert','SigmaTT_uncert','SigmaLT_uncert'])
    # print("DF IS ----------")
    # print(df)
    # df.to_pickle(t_pkl_dir+fs["phi_fits_pkl_name"])


def iterate_3var_counts_single_with_t(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,plot_out_dir,dataframe,
                    t_pkl_dir="t_pkls/",pkl_filename="pkl_out.pkl"):

    t_vals = []

    data = dataframe
    
    fs = filestruct.fs()
    
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs.__getattribute__(iter_var_bins[0]) #t
    var2_bins = fs.__getattribute__(iter_var_bins[1]) #xb
    var3_bins = fs.__getattribute__(iter_var_bins[2]) #q2



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

                ic(data_filtered)

                phi_bins = np.array(data_filtered["phi_min"])#.tolist()#+[360,]
                bin_counts_0 = np.array(data_filtered["counts"])#.tolist()
                bin_corr_fact = np.array(data_filtered["counts_acc_factor"])#.tolist()
                bin_corr_fact_uncert = np.array(data_filtered["counts_acc_factor_uncert"])#.tolist()

                ic.disable()
                ic(bin_counts_0)
                ic(bin_corr_fact)
                ic(bin_corr_fact_uncert)


                
                ic.disable()
                ic(bin_counts_0)
                ic(phi_bins)
                ##ic.enable()
                
                bbl = bin_bound_labels
                plot_title = '{}_fit_{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                dir_ind = "0"+str(var1_ind-1) if (var1_ind-1)<10 else str(var1_ind-1)
                plot_out_dir_new = plot_out_dir + "t" + dir_ind+"/"


                
                ##ic.enable()
                #ic(plot_out_dir)
                fit_params, fit_cov, chisq, p = phi_Fitter.getPhiFit_prebinned(phi_bins,bin_counts_0,plot_title,plot_out_dir_new,args,bin_corr_fact,bin_corr_fact_uncert)
                
                #ic.enable()
                ic(chisq)
                ic.disable()
                ic(fit_params)
                #phi_Fitter.plotPhi_single(phi_bins,bin_counts_0,plot_title,plot_out_dir_new,args)

                bb = bin_bounds

                if chisq == "nofit":
                    t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                            0,0,0,0,0,0,
                            0,0,0,0,0,
                            0,0,0])

                else:
                    A,B,C = fit_params[0],fit_params[1],fit_params[2]


                    qmod = 1
                    amod = np.sqrt(np.square(chisq))/20

                    #ic.enable()
                    ic(amod)
                    if amod > 1:
                        qmod = amod
                    
                    a_err = np.sqrt(fit_cov[0][0])*qmod
                    b_err = np.sqrt(fit_cov[1][1])*qmod
                    c_err = np.sqrt(fit_cov[2][2])*qmod

                    
                    sigmaTeL = A
                    sigmaTT = B
                    sigmaLT = C

            
                    sigmaTeL_uncert = a_err
                    sigmaTT_uncert = b_err
                    sigmaLT_uncert = c_err

                                    #xb,  #xb, #q2, q3,   t, t
                    t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                            A,B,C,a_err,b_err,c_err,
                            chisq,p,sigmaTeL,sigmaTT,sigmaLT,
                            sigmaTeL_uncert,sigmaTT_uncert,sigmaLT_uncert])

    print("out of loop")  
    ic.enable()
    ic(t_vals)
    col_names = ['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax',
                            'A','B','C','A_uncert','B_uncert','C_uncert','ChiSq','P',
                            'SigmaTeL','SigmaTT','SigmaLT',
                            'SigmaTeL_uncert','SigmaTT_uncert','SigmaLT_uncert']
    print(len(col_names))
    df = pd.DataFrame(t_vals, columns=col_names)
    print("DF IS ----------")
    print(df)
    df.to_pickle(t_pkl_dir+fs.phi_fits_pkl_name_corrected)
    print("saved to {} ".format(t_pkl_dir+fs.phi_fits_pkl_name_corrected))


def iterate_3var_counts_double(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,plot_out_dir,dataframe0,dataframe1):

    t_vals = []

    data = dataframe0
    data_1 = dataframe1
    
    fs = filestruct.fs()
    
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs.__getattribute__(iter_var_bins[0]) #t
    var2_bins = fs.__getattribute__(iter_var_bins[1]) #xb
    var3_bins = fs.__getattribute__(iter_var_bins[2]) #q2



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
                data_filtered1 = data_1.query(dfq)[1:]     

                #ic(data_filtered)
                #ic(data_filtered1)

                phi_bins = data_filtered["phi_min"].tolist()+[360,]
                bin_counts_0 = data_filtered["counts"].tolist()
                bin_counts_1 = data_filtered1["counts_corrected"].tolist()
                
                ##ic.enable()
                
                bbl = bin_bound_labels
                plot_title = '{}_fit_{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                dir_ind = "0"+str(var1_ind-1) if (var1_ind-1)<10 else str(var1_ind-1)
                plot_out_dir_new = plot_out_dir + "t" + dir_ind+"/"


                
                ##ic.enable()
                #ic(plot_out_dir)
                #fit_params, fit_cov, chisq, p = phi_Fitter.getPhiFit_prebinned(phi_bins,bin_counts,plot_title,plot_out_dir_new,args)
                
                phi_Fitter.plotPhi_duo(phi_bins,bin_counts_0,bin_counts_1,plot_title,plot_out_dir_new,args)

                # bb = bin_bounds

                # if chisq == "nofit":
                #     t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                #             0,0,0,0,0,0,
                #             0,0,0,0,0,0,0,
                #             0,0,0])

                # else:
                #     A,B,C = fit_params[0],fit_params[1],fit_params[2]
                #     a_err = np.sqrt(fit_cov[0][0])
                #     b_err = np.sqrt(fit_cov[1][1])
                #     c_err = np.sqrt(fit_cov[2][2])
                    
                #     q2_mid = (bb[4]+bb[5])/2
                #     xb_mid = (bb[2]+bb[3])/2
                #     E = 10.6
                #     Eprime = 3

                #     Gamma, Epsilon = gamma_epsilon_calculator.calculate_gamma_epsilon(q2_mid,xb_mid,E,Eprime)

                #     sigmaTeL = A/Gamma
                #     sigmaTT = B/(Gamma*Epsilon)
                #     sigmaLT = C/(Gamma*np.sqrt(2*Epsilon*(1+Epsilon)))

            
                #     sigmaTeL_uncert = a_err/A*sigmaTeL 
                #     sigmaTT_uncert = b_err/B*sigmaTT 
                #     sigmaLT_uncert = c_err/C*sigmaLT 


                #                     #xb,  #xb, #q2, q3,   t, t
                #     t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                #             A,B,C,a_err,b_err,c_err,
                #             chisq,p,Gamma,Epsilon,sigmaTeL,sigmaTT,sigmaLT,
                #             sigmaTeL_uncert,sigmaTT_uncert,sigmaLT_uncert])
                                
    # df = pd.DataFrame(t_vals, columns=['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax',
    #                         'A','B','C','A_uncert','B_uncert','C_uncert','ChiSq','P',
    #                         'Gamma','Epsilon','SigmaTeL','SigmaTT','SigmaLT',
    #                         'SigmaTeL_uncert','SigmaTT_uncert','SigmaLT_uncert'])
    # print("DF IS ----------")
    # print(df)
    # df.to_pickle(t_pkl_dir+fs["phi_fits_pkl_name"])



def iterate_3var_counts_acc_maker(args,iter_vars,iter_var_bins,plotting_vars,plotting_ranges,plot_out_dir,dataframe0,dataframe1,df_real):

    t_vals = []

    data = dataframe0
    data_1 = dataframe1
    real_df = df_real
    
    fs = filestruct.fs()
    
    file_maker.make_dir(plot_out_dir)
    
    var1_bins = fs.__getattribute__(iter_var_bins[0]) #t
    var2_bins = fs.__getattribute__(iter_var_bins[1]) #xb
    var3_bins = fs.__getattribute__(iter_var_bins[2]) #q2



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
                data_filtered1 = data_1.query(dfq)   

                ic.enable()
                ic(data_filtered)
                ic(data_filtered1)
                sys.exit()

                phi_bins = data_filtered["phi_min"].tolist()+[360,]
                bin_counts_0 = data_filtered["counts"].tolist()
                bin_counts_1 = data_filtered1["counts"].tolist()
                
                ##ic.enable()
                
                bbl = bin_bound_labels
                plot_title = '{}_fit_{}-{}-{}-{}-{}-{}-{}-{}-{}'.format(plotting_vars[0],
                    iter_vars[0],bbl[0],bbl[1],iter_vars[1],bbl[2],bbl[3],iter_vars[2],bbl[4],bbl[5])


                dir_ind = "0"+str(var1_ind-1) if (var1_ind-1)<10 else str(var1_ind-1)
                plot_out_dir_new = plot_out_dir + "t" + dir_ind+"/"


                
                ##ic.enable()
                #ic(plot_out_dir)
                #fit_params, fit_cov, chisq, p = phi_Fitter.getPhiFit_prebinned(phi_bins,bin_counts,plot_title,plot_out_dir_new,args)
                
                phi_Fitter.plotPhi_duo(phi_bins,bin_counts_0,bin_counts_1,plot_title,plot_out_dir_new,args)

                # bb = bin_bounds

                # if chisq == "nofit":
                #     t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                #             0,0,0,0,0,0,
                #             0,0,0,0,0,0,0,
                #             0,0,0])

                # else:
                #     A,B,C = fit_params[0],fit_params[1],fit_params[2]
                #     a_err = np.sqrt(fit_cov[0][0])
                #     b_err = np.sqrt(fit_cov[1][1])
                #     c_err = np.sqrt(fit_cov[2][2])
                    
                #     q2_mid = (bb[4]+bb[5])/2
                #     xb_mid = (bb[2]+bb[3])/2
                #     E = 10.6
                #     Eprime = 3

                #     Gamma, Epsilon = gamma_epsilon_calculator.calculate_gamma_epsilon(q2_mid,xb_mid,E,Eprime)

                #     sigmaTeL = A/Gamma
                #     sigmaTT = B/(Gamma*Epsilon)
                #     sigmaLT = C/(Gamma*np.sqrt(2*Epsilon*(1+Epsilon)))

            
                #     sigmaTeL_uncert = a_err/A*sigmaTeL 
                #     sigmaTT_uncert = b_err/B*sigmaTT 
                #     sigmaLT_uncert = c_err/C*sigmaLT 


                #                     #xb,  #xb, #q2, q3,   t, t
                #     t_vals.append([bb[2],bb[3],bb[4],bb[5],bb[0],bb[1],
                #             A,B,C,a_err,b_err,c_err,
                #             chisq,p,Gamma,Epsilon,sigmaTeL,sigmaTT,sigmaLT,
                #             sigmaTeL_uncert,sigmaTT_uncert,sigmaLT_uncert])
                                
    # df = pd.DataFrame(t_vals, columns=['xBmin', 'xBmax', 'Q2min','Q2max','tmin','tmax',
    #                         'A','B','C','A_uncert','B_uncert','C_uncert','ChiSq','P',
    #                         'Gamma','Epsilon','SigmaTeL','SigmaTT','SigmaLT',
    #                         'SigmaTeL_uncert','SigmaTT_uncert','SigmaLT_uncert'])
    # print("DF IS ----------")
    # print(df)
    # df.to_pickle(t_pkl_dir+fs["phi_fits_pkl_name"])




def iterate_4var_acc_maker(args,iter_vars,iter_var_bins,
    dataframe_sim,dataframe_lund,dataframe_real,t_pkl_dir="t_pkls/",pkl_filename="pkl_out.pkl"):

    count_vals = []


    fs = filestruct.fs()
    
    file_maker.make_dir(t_pkl_dir)
    
    var1_bins = fs.__getattribute__(iter_var_bins[0]) #phi
    var2_bins = fs.__getattribute__(iter_var_bins[1]) #t
    var3_bins = fs.__getattribute__(iter_var_bins[2]) #xb
    var4_bins = fs.__getattribute__(iter_var_bins[3]) #q2

    total_counts = 0
    ic.disable()

    #ic.enable()
    for var4_ind in range(0,len(var4_bins)):
        print("on {} index {}".format(iter_var_bins[3],var4_ind))
        var4_min = var4_bins[var4_ind-1]
        var4_max = var4_bins[var4_ind]    

        for var3_ind in range(0,len(var3_bins)):
            print("on {} index {}".format(iter_var_bins[2],var3_ind))
            var3_min = var3_bins[var3_ind-1]
            var3_max = var3_bins[var3_ind]
          
            
            for var2_ind in range(0,len(var2_bins)):
                ##print"on {} index {}".format(iter_var_bins[1],var2_ind))
                var2_min = var2_bins[var2_ind-1]
                var2_max = var2_bins[var2_ind]
                

                for var1_ind in range(0,len(var1_bins)):
                    var1_min = var1_bins[var1_ind-1]
                    var1_max = var1_bins[var1_ind]


                                    #phi    #phi      #t    #t         #xb      #xb      #q2     #q2
                    bin_bounds = [var1_min,var1_max,var2_min,var2_max,var3_min,var3_max,var4_min,var4_max]
                    bin_bound_labels = [str(bin_end) for bin_end in bin_bounds]
        
                    for ind,bin_end in enumerate(bin_bound_labels):
                        if bin_bounds[ind]<10 and bin_bounds[ind]>=1:
                            bin_bound_labels[ind] = "0"+bin_end


                    dfq = query_maker.make_query(iter_vars,bin_bounds)
                    
                    counts_sim_df = dataframe_sim.query(dfq)
                    counts_gen_df = dataframe_lund.query(dfq)
                    counts_real_df = dataframe_real.query(dfq)

                    #ic.enable()
                    num_sim = (counts_sim_df["counts"].sum())
                    num_gen =(counts_gen_df["counts"].sum())
                    num_real =(counts_real_df["counts"].sum())


                    counts_corrected = 0

                    if num_sim + num_gen + num_real > 0:
                        

                        counts_sim_0 = counts_sim_df["counts"].values[0]
                        counts_gen_0 = counts_gen_df["counts"].values[0]
                        counts_real = counts_real_df["counts"].values[0]

                        # ic(counts_sim_df)
                        # ic(counts_gen_df)
                        # ic(counts_real_df)
                   

                        if counts_sim_0 < 1:
                            counts_sim = 1
                        if counts_gen_0 < 1:
                            counts_gen = 1

                        counts_corrected = counts_real * counts_gen/counts_sim

                        #ic(counts_corrected)

                        #input("continue")


                
                    count_vals.append([var4_min,var4_max,var3_min,var3_max,var2_min,var2_max,var1_min,var1_max,counts_corrected])

    df = pd.DataFrame(count_vals, columns=['Q2min','Q2max','xBmin', 'xBmax', 'tmin','tmax','phi_min','phi_max','counts_corrected'])
    print("DF IS ----------")
    ic.enable()
    print("Saved pickled df to {}".format(t_pkl_dir+"corrected_"+pkl_filename))
    df.to_pickle(t_pkl_dir+pkl_filename)
    total_counts = 0
    ic(df["counts_corrected"].sum())
    ##ic.enable()
    #ic(df)
    
                    
   

def iterate_4var(args,iter_vars,iter_var_bins,
    datafile,t_pkl_dir="t_pkls/",pkl_filename="pkl_out.pkl"):

    count_vals = []

    data=datafile

    fs = filestruct.fs()
    
    file_maker.make_dir(t_pkl_dir)
    
    var1_bins = fs.__getattribute__(iter_var_bins[0]) #phi
    var2_bins = fs.__getattribute__(iter_var_bins[1]) #t
    var3_bins = fs.__getattribute__(iter_var_bins[2]) #xb
    var4_bins = fs.__getattribute__(iter_var_bins[3]) #q2

    ic.disable()
    ic(var1_bins)
    ic(var2_bins)
    ic(var3_bins)
    ic(var4_bins)


    total_counts = 0
    ic.disable()

    #ic.enable()
    for var4_ind in range(1,len(var4_bins)):
        print("on {} index {}".format(iter_var_bins[3],var4_ind))
        var4_min = var4_bins[var4_ind-1]
        var4_max = var4_bins[var4_ind]    

        for var3_ind in range(1,len(var3_bins)):
            print("on {} index {}".format(iter_var_bins[2],var3_ind))
            var3_min = var3_bins[var3_ind-1]
            var3_max = var3_bins[var3_ind]
          
            
            for var2_ind in range(1,len(var2_bins)):
                ##print"on {} index {}".format(iter_var_bins[1],var2_ind))
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
                    ic.disable()
                    num_events = len(data_filtered.index)
                    #print(num_events)
                    #ic.enable()

                    

                    gamma = -1
                    epsi = -1

                    if num_events>0:
                        total_counts +=num_events
                        #ic.enable()
                        ic(total_counts)
                        ic.disable()
                        ic(data_filtered['gamma'])
                        gamma = data_filtered['gamma'].mean()
                        epsi = data_filtered['epsi'].mean()
                        
                        ic(epsi)

                        ic(num_events)


                    count_vals.append([var4_min,var4_max,var3_min,var3_max,var2_min,var2_max,var1_min,var1_max,num_events,gamma,epsi])

    df = pd.DataFrame(count_vals, columns=['Q2min','Q2max','xBmin', 'xBmax', 'tmin','tmax','phi_min','phi_max','counts','gamma','epsi'])
    print("DF IS ----------")
    ic.enable()
    total_counts = 0
    ic(df["counts"].sum())
    ic.enable()
    ic(df)
    df.to_pickle(t_pkl_dir+"gamma_ep_"+pkl_filename)
    print("Saved pickled df to {}".format(t_pkl_dir+"gamma_ep_"+pkl_filename))
                    
                    

if __name__ == "__main__":
    print("no iterator fuction defined")