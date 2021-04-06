#!/usr/bin/env python3
"""
A simple script to save Z and X of 6862 nflow project.
"""

import uproot
import pandas as pd
import numpy as np
import argparse
import os, sys
from icecream import ic
import matplotlib.pyplot as plt
from copy import copy
from utils.utils import dot
from utils.utils import mag
from utils.utils import mag2
from utils.utils import cosTheta
from utils.utils import angle
from utils.utils import cross
from utils.utils import vecAdd
from utils.utils import pi0Energy
from utils.utils import pi0InvMass
from utils.utils import getPhi
from utils.utils import getTheta
from utils.utils import getEnergy
from utils.utils import readFile
from utils import make_histos


gen = pd.read_pickle("final_binning/all_gen_binned.pkl")
recon = pd.read_pickle("final_binning/recon_phi_binned.pkl")
final = pd.read_pickle("final_binning/real_phi_binned.pkl")

final.loc[:, "recon_counts"] = recon.loc[:, "recon_counts"]
final.loc[:, "gen_counts"] = gen.loc[:, "gen_counts"]



final.loc[:, "acc"] = final.loc[:, "recon_counts"]/final.loc[:, "gen_counts"]
final.loc[:, "real_corr"] = final.loc[:, "real_counts"]/final.loc[:, "acc"]
final.loc[:, "real_corr"] =final.loc[:, "real_corr"].fillna(0)
ic(final)

final_0 = final.query("tmin==0.2")

ic(final_0)
ic(final_0.index)


def plotPhi_duo(phi_bins,bin_counts_0,bin_counts_1,phi_title,plot_dir,saveplot=False):

    ic(phi_bins)
    
    
    data_entries_0 = bin_counts_0
    data_entries_1 = bin_counts_1
    bins = phi_bins

    data_errors_0 = np.sqrt(data_entries_0)
    data_errors_0 = [1/err if err>0 else err+1 for err in data_errors_0]

    data_errors_1 = np.sqrt(data_entries_1)
    data_errors_1 = [1/err if err>0 else err+1 for err in data_errors_1]

    #print(data_entries)

    if 1==1:
        ic(bins)
        binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
        binscenters = np.append(binscenters,np.array([351,]),axis=0)
        ic(binscenters)
        # 5.) Fit the function to the histogram data.
        #popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=data_entries, p0=[2.0, 2, 0.3],
         #           sigma=data_errors, absolute_sigma=True)
        #print(popt) #popt contains the values for A, B, C

        ##a_err = np.sqrt(pcov[0][0])
        ##b_err = np.sqrt(pcov[1][1])
        #c_err = np.sqrt(pcov[2][2])

        #a,b,c = popt[0],popt[1],popt[2]
        #ic(a_err,b_err,c_err)
        #ic.disable()
        
        # 6.)
        # Generate enough x values to make the curves look smooth.
       
        #fit_y_data_1 = fit_function(binscenters, *popt)

        #ic(fit_y_data_1)

        

        #chisq0 = stats.chisquare(f_obs=data_entries, f_exp=fit_y_data_1)
        #chisq = stats.chisquare(f_obs=np.array(data_entries, dtype=np.float64), f_exp=np.array(fit_y_data_1, dtype=np.float64))

        #sums=[]
        #for ind,val in enumerate(fit_y_data_1):
        #    diff2 = (data_entries[ind]-val)**2
        #    s1 = diff2/val
        #    sums.append(s1)

       # manchisq = np.sum(sums)

        ###ic.enable()
        #if chisq0[0]<0:
        #    ic(manchisq)
        #    ic(chisq0[0])
        #if not (chisq0[0] == chisq[0]):
        #    print("ERROR MISMATCH")
        #    print(chisq0[0])
        #    print(chisq[0])
        #    print(manchisq)


       # p = chisq[1]
       # chisq = chisq[0]

        ##ic(chisq)
        #ic(p)


        #xspace = np.linspace(0, xmax, 1000)
        #fit_y_data = fit_function(xspace, *popt)

        ##ic.enable()
        #ic(fit_y_data)
        
        #y_manual = []
        #for ind, val in enumerate(xspace):
        #    ic(val,a,b,c)
        #    y_one = fit_function(val,a,b,c)
        #    ic(y_one)
        #    y_manual.append(y_one)


        
        #7
        # Plot the histogram and the fitted function.

        fig = plt.figure()
        ax = fig.add_subplot(111)
        


        highPower = data_entries_0
        lowPower = data_entries_1


        #plt.bar(binscenters, highPower,  
        #        color='b', label='LUND Events')
        #plt.bar(binscenters,  lowPower, color='r', alpha=0.5, label='Sim Events')




        #ic.enable()
        #ic(binscenters)
        #ic(data_entries_0)
        #ic(data_entries_1)
        bar0 = ax.bar(binscenters, data_entries_1, width=bins[1] - bins[0], color='red', label='Raw Counts')
        bar1 = ax.bar(binscenters, data_entries_0, width=bins[1] - bins[0], color='black', label='With Acceptance Corr.')
       # fit1, = ax.plot(xspace, fit_y_data, color='darkorange', linewidth=2.5, label='Fitted function')


        # Make the plot nicer.
        plt.xlim(0,360)
        #plt.ylim(0,5)
        plt.xlabel(r'phi')
        plt.ylabel(r'Number of entries')

        plot_title = plot_dir + phi_title+".png"
        plt.title(phi_title)
        #plt.legend(loc='best')
        plt.legend()


        #fit_params = "A: {:2.2f} +/- {:2.2f}\n B:{:2.2f} +/- {:2.2f}\n C:{:2.2f} +/- {:2.2f}\n Chi:{:2.2f} \n p:{:2.2f}".format(a,a_err,b,b_err,c,c_err,chisq,p)


        #plt.text(120, max(data_entries)/1.3, fit_params)

        
        if saveplot:
            plt.savefig(plot_title)
            plt.close()
        else:
            plt.show()
            plt.close()
        #print("plot saved to {}".format(plot_title))


plotPhi_duo(final_0.index,final_0["real_counts"],final_0["real_corr"],"real vs real corr","pics/",)
plotPhi_duo(final_0.index,final_0["recon_counts"],final_0["gen_counts"],"recon vs gen","pics/",)
