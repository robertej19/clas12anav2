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

from src.utils import filestruct
from src.utils import file_maker


def plot_t_dep(data,plot_out_dirname,xb_ranges,q2_ranges,ice_cream_enable):

    
    fs = filestruct.fs()

    lumi = fs.f18_inbending_total_lumi

    cm2_to_nb = 1e-24*1e-9

    ic.disable()
    if ice_cream_enable:
        ic.enable()

    plot_out_dirpath = fs.base_dir+fs.output_dir+fs.t_dep_dir+plot_out_dirname
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

            

            y = data_t["SigmaTeL"]/lumi/cm2_to_nb
            z = data_t["SigmaTT"]/lumi/cm2_to_nb
            w = data_t["SigmaLT"]/lumi/cm2_to_nb
            qq = data_t["SigmaTeL"]/lumi/cm2_to_nb

            y_err = data_t["SigmaTeL_uncert"]/lumi/cm2_to_nb
            z_err = data_t["SigmaTT_uncert"]/lumi/cm2_to_nb
            w_err = data_t["SigmaLT_uncert"]/lumi/cm2_to_nb

            
            ic(y_err)
            #sys.exit()
            #A = T+L, B=TT, C=LT
            #A = black, B=blue, C=red
            fig, ax = plt.subplots()
            ax.errorbar(x,y,fmt='k',yerr=y_err,marker='o',linestyle="None", ms=10,label="A - t+l")
            ax.errorbar(x,z,fmt='b',yerr=z_err,marker='o',linestyle="None", ms=10,label="B - tt")
            ax.errorbar(x,w,fmt='r',yerr=w_err,marker='o',linestyle="None", ms=10,label="C - lt")

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


def plot_t_dep_with_clas(data,clas6_data,plot_out_dirname,xb_ranges,q2_ranges,ice_cream_enable,g_ep_df="none"):

    
    fs = filestruct.fs()

    lumi = fs.f18_inbending_total_lumi

    cm2_to_nb = 1e-24*1e-9

    ic.disable()
    if ice_cream_enable:
        ic.enable()

    plot_out_dirpath = fs.base_dir+fs.output_dir+fs.t_dep_dir+plot_out_dirname
    file_maker.make_dir(plot_out_dirpath)

    ic.enable()
    ic(data)

    for xb_ind in range(0,len(xb_ranges)-1):
        xBmax = xb_ranges[xb_ind+1]
        print("Making t-dep plots for xb = {}".format(xBmax))
        for q2_ind in range(0,len(q2_ranges)-1):
            Q2max = q2_ranges[q2_ind+1]



            ic.disable()

            
            ic(xBmax)
            ic(Q2max)
            data_t = data[(data['Q2max']==Q2max) & (data['xBmax']==xBmax)]
            #data_t = data[data['Q2max']==xBmax]

            data_t = data_t[:-2]
            #ic.enable()
            #ic(data_t)
            #sys.exit()
            ic(clas6_data)

            q_string = "q2 > {} and q2 < {} and xb > {} and xb < {}".format(q2_ranges[q2_ind],Q2max,xb_ranges[xb_ind],xBmax)
            
            ge_ep_q_string = "Q2max == {} and xBmax =={}".format(Q2max,xBmax)
            
            ic(q_string)
            clas6_vals = clas6_data.query(q_string)
            g_ep_df_vals = g_ep_df.query(ge_ep_q_string)

            ic(g_ep_df_vals)

            
          
            

            x = data_t["tmax"]

            ic(x)

            gamma_vals = []
            epsi_vals = []
            epsi_vals_lt = []
            for tmax_val in x:
                t_q = "tmax == {}".format(tmax_val)
                g_ep_df_vals_t = g_ep_df_vals.query(t_q)
            
                gamma_val = np.sqrt(g_ep_df_vals_t['gamma']**2).mean()
                if gamma_val == -1:                    
                    gamma_val = 1
                epsi_val = np.sqrt(g_ep_df_vals_t['epsi']**2).mean()
                if epsi_val == -1:
                    epsi_val = 1
                ic.disable()
                ic(gamma_val)
                ic.disable()
                epsi_val_lt = np.sqrt(2*epsi_val*(1+epsi_val))
                
                ic(epsi_val_lt)
                ic(g_ep_df_vals_t)
                ic(epsi_val)

                ic(gamma_val)
                gamma_vals.append(gamma_val)
                epsi_vals.append(epsi_val)
                epsi_vals_lt.append(epsi_val_lt)

            ic(gamma_vals)
            ic(epsi_vals)
            ic(epsi_vals_lt)


            

            ic(epsi_val_lt)

            # y = data_t["A"]
            # z = data_t["B"]
            # w = data_t["C"]
            
            # y_err = data_t["A_uncert"]
            # z_err = data_t["B_uncert"]
            # w_err = data_t["C_uncert"]

            

            y = data_t["SigmaTeL"]/lumi/cm2_to_nb/gamma_vals
            z = data_t["SigmaTT"]/lumi/cm2_to_nb/gamma_vals/epsi_vals
            w = data_t["SigmaLT"]/lumi/cm2_to_nb/gamma_vals/epsi_vals_lt

            y_err = data_t["SigmaTeL_uncert"]/lumi/cm2_to_nb/gamma_vals
            z_err = data_t["SigmaTT_uncert"]/lumi/cm2_to_nb/gamma_vals/epsi_vals
            w_err = data_t["SigmaLT_uncert"]/lumi/cm2_to_nb/gamma_vals/epsi_vals_lt

            qq = y/gamma_vals
            ic(y)
            ic(qq)
            ic(y)
            ic(z)
            

            ic(y_err)
            #sys.exit()
            #A = T+L, B=TT, C=LT
            #A = black, B=blue, C=red
            fig, ax = plt.subplots()

            #ic.enable()
            #ic(x)
            #ic(max(x))
            #sys.exit()
            if not ((max(y)==0) and (max(z)==0) and (max(w)==0)):
                ax.errorbar(x,y,fmt='k',yerr=y_err,marker='d',linestyle="None", ms=10,label="CLAS12 - t+l")
                ax.errorbar(x,z,fmt='b',yerr=z_err,marker='d',linestyle="None", ms=10,label="CLAS12 - tt")
                ax.errorbar(x,w,fmt='r',yerr=w_err,marker='d',linestyle="None", ms=10,label="CLAS12 - lt")


            if not clas6_vals.empty:
                #print("im not empty")
                ic(clas6_vals)
                
                x_c6 = clas6_vals["t"]
                tel_c6 = clas6_vals["tel"]
                tel_err_c6 = np.sqrt(np.square(clas6_vals["telstat"])+np.square(clas6_vals["telsys"]))

                lt_c6 = clas6_vals["lt"]
                lt_err_c6 = np.sqrt(np.square(clas6_vals["ltstat"])+np.square(clas6_vals["ltsys"]))

                tt_c6 = clas6_vals["tt"]
                tt_err_c6 = np.sqrt(np.square(clas6_vals["ttstat"])+np.square(clas6_vals["ttsys"]))

                ic(clas6_vals["telstat"])
                ic(clas6_vals["telsys"])
                ic(tel_err_c6)

                ax.errorbar(x_c6,tel_c6,fmt='k',yerr=tel_err_c6,marker='x',linestyle="None", ms=10,label="CLAS6 - t+l")
                ax.errorbar(x_c6,lt_c6,fmt='r',yerr=lt_err_c6,marker='x',linestyle="None", ms=10,label="CLAS6 - lt")
                ax.errorbar(x_c6,tt_c6,fmt='b',yerr=tt_err_c6,marker='x',linestyle="None", ms=10,label="CLAS6 - tt")



            Q2maxstr = str(Q2max)
            if len(Q2maxstr) < 4:
                #print("Q2maxstr is {} adding a 0 to yield: ".format(Q2maxstr))
                Q2maxstr = "0"+Q2maxstr
                #print(Q2maxstr)
            #if len(Q2max) < 2:
            #    q2max = "0"+q2max

            t_title = 't-dependence-xb-{}-q2-{}'.format(xBmax,Q2maxstr)

            plt.title(t_title)
            if not ((max(y)==0) and (max(z)==0) and (max(w)==0)):
                plt.legend(loc='best')
            plt.xlabel(r't (GeV^2)')
            plt.ylabel('cross section (nb/GeV^2)')

            #plt.ylim(top=500) #ymax is your value
            #plt.ylim(bottom=-400) #ymin is your value

            
            plot_title = plot_out_dirpath + t_title+".png"
            #print(plot_title)
            plt.savefig(plot_title)
            #plt.show()
            #sys.exit()

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

