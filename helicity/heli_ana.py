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


M = 0.938272081 # target mass
me = 0.5109989461 * 0.001 # electron mass
ebeam = 10.604 # beam energy
pbeam = np.sqrt(ebeam * ebeam - me * me) # beam electron momentum
beam = [0, 0, pbeam] # beam vector
target = [0, 0, 0] # target vector
   
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f","--fname", help="a single root file to convert into pickles", default="infile.root")
    parser.add_argument("-o","--out", help="a single pickle file name as an output", default="outfile.pkl")
    parser.add_argument("-s","--entry_stop", help="entry_stop to stop reading the root file", default = None)
    
    args = parser.parse_args()

    # t ranges:
    # 0.2 - 0.3, .4, .6, 1.0
    # xb ranges:
    # 0.25, 0.3, 0.38
    # q2 ranges:
    # 3, 3.5, 4, 4.5

    # #xxxxxxxxxxxxxxxxxxxxxxxxxxx
    # #Push though the REAL data
    # #xxxxxxxxxxxxxxxxxxxxxxxxxxx
    #df_real = pd.read_pickle("df_real.pkl")
    #df_after_cuts = pd.read_pickle("df_real_5000_5099.pkl")
    df_after_cuts = pd.read_pickle("../newpandas/ana_pandas/real/F18_All_DVPi0_Events.pkl")
    #ic(df_real)

    #make plots after cuts are applied
    ic(df_after_cuts.head(5))
    #hist = df_after_cuts.hist(bins=30)
    #plt.show()
    ic(df_after_cuts.columns.values)

    sys.exit()


    alpha = 1/137 #Fund const
    mp = 0.938 #Mass proton
    prefix = alpha/(8*np.pi)
    E = 10.6

    epsilon = 0.5

    
    df_after_cuts.loc[:, "y"] = (E-df_after_cuts.loc[:, "nu"])/E

    df_after_cuts.loc[:, "q24E2"] = df_after_cuts.loc[:, "Q2"]/(4*E*E)
    df_after_cuts.loc[:, "epsi"] = (1-df_after_cuts.loc[:, "y"]-df_after_cuts.loc[:, "q24E2"])/(1-df_after_cuts.loc[:, "y"]+(df_after_cuts.loc[:, "q24E2"]*df_after_cuts.loc[:, "q24E2"])/2+df_after_cuts.loc[:, "q24E2"])
    df_after_cuts.loc[:, "gamma"] = prefix*df_after_cuts.loc[:, "Q2"]/(mp*mp*E*E)*(1-df_after_cuts.loc[:,"xB"])/(df_after_cuts.loc[:,"xB"]**3)*(1/(1- df_after_cuts.loc[:, "epsi"]))/(2*np.pi)


    ic(df_after_cuts.head(5))




    
    #df_small_gen = df_after_cuts
    def get_counts(tmin,tmax):
        tmin = tmin
        tmax = tmax
        xbmin = 0.3
        xbmax = 0.38
        q2min = 3
        q2max = 3.5
        cut_q = "xB>{} & xB<{} & Q2>{} & Q2<{} & t>{} & t<{}".format(xbmin,xbmax,q2min,q2max,tmin,tmax)
        df_small_gen = df_after_cuts.query(cut_q)
        ic(df_small_gen)

        

        x_data = df_small_gen["phi1"]
        var_names = ["$\phi$"]
        ranges = [0,360,20]
        output_dir = "pics/"
        title = "$\phi$, F18In, {}<t<{} GeV$^2$,{}<$x_B$<{}, {}<$Q^2$<{}".format(tmin,tmax,xbmin,xbmax,q2min,q2max)
        make_histos.plot_1dhist(x_data,var_names,ranges,
                        saveplot=True,pics_dir=output_dir,plot_title=title.replace("/",""),first_color="darkslateblue")

        count, division = np.histogram(x_data, bins = [0,18,36,54,72,90,108,126,144,162,180,198,216,234,252,270,288,306,324,342,360])
        print(count)
        print(division)
        print(len(division))
        print(len(count))
        print(np.sum(count))
        tmin_arr = tmin*np.ones(len(count))
        mean_g = df_small_gen['gamma'].mean()*np.ones(len(count))
        mean_epsi = df_small_gen['epsi'].mean()*np.ones(len(count))
        return count, tmin_arr, mean_g, mean_epsi, division

    count, tmin_arr, mean_g, mean_epsi,division = get_counts(0.2,0.3)

    binned = pd.DataFrame(data=tmin_arr,index=division[:-1],columns=['tmin'])
    binned['real_counts'] = count
    binned['gamma'] = mean_g
    binned['epsi'] = mean_epsi
    ic(binned)

    count, tmin_arr, mean_g, mean_epsi, division = get_counts(0.3,0.5)
    binned2 = pd.DataFrame(data=tmin_arr,index=division[:-1],columns=['tmin'])
    binned2['real_counts'] = count
    binned2['gamma'] = mean_g
    binned2['epsi'] = mean_epsi
    ic(binned2)

    count, tmin_arr, mean_g, mean_epsi,division = get_counts(0.5,1.0)
    binned3 = pd.DataFrame(data=tmin_arr,index=division[:-1],columns=['tmin'])
    binned3['real_counts'] = count
    binned3['gamma'] = mean_g
    binned3['epsi'] = mean_epsi
    ic(binned3)

    real_out = pd.concat([binned,binned2,binned3])
    ic(real_out)

    real_out.to_pickle("real_phi_binned.pkl")


    # x_data = df_small_gen["gamma"]
    # var_names = ["$\Gamma$"]
    # ranges = [0.0002, 0.0018, 30]
    # output_dir = "pics/"
    # title = "$\Gamma$ for {}<t<{} GeV$^2$, {}<$x_B$<{}, {}<$Q^2$<{}".format(tmin,tmax,xbmin,xbmax,q2min,q2max)
    # make_histos.plot_1dhist(x_data,var_names,ranges,
    #                 saveplot=True,pics_dir=output_dir,plot_title=title.replace("/",""),first_color="darkslateblue",sci_on=True)

    # x_data = df_small_gen["epsi"]
    # var_names = ["$\epsilon$"]
    # ranges = [.966,.974, 30]
    # output_dir = "pics/"
    # title = "$\epsilon$ for {}<t<{} GeV$^2$,{}<$x_B$<{}, {}<$Q^2$<{}".format(tmin,tmax,xbmin,xbmax,q2min,q2max)
    # make_histos.plot_1dhist(x_data,var_names,ranges,
    #                 saveplot=True,pics_dir=output_dir,plot_title=title.replace("/",""),first_color="darkslateblue")


    #hist = df_small_gen.hist(bins=30)
    #plt.show()
    #sys.exit()
    x_data2 = df_small_gen["phi1"]
    var_names = ["phi"]


    # y_data = df_small_gen["Ptheta"]
    # x_data = df_small_gen["Pphi"]
    # var_names = ["phi","theta"]
    # ranges = [-180,180,180,0,50,50]
    output_dir = "./pics"
    lund_q2_xb_title = "$\phi$ Distribution, F18 In data"

    # make_histos.plot_2dhist(x_data,y_data,var_names,ranges,colorbar=True,
    #                 saveplot=False,pics_dir=output_dir,plot_title=lund_q2_xb_title.replace("/",""))


    # y_data = df_small_gen["Etheta"]
    # x_data = df_small_gen["Ephi"]
    # lund_q2_xb_title = "Electron angles for {}".format("here/")

    # make_histos.plot_2dhist(x_data,y_data,var_names,ranges,colorbar=True,
    #                 saveplot=False,pics_dir=output_dir,plot_title=lund_q2_xb_title.replace("/",""))

    # y_data = df_small_gen["Gtheta"]
    # x_data = df_small_gen["Gphi"]
    # lund_q2_xb_title = "Photon angles for {}".format("here/")

    # make_histos.plot_2dhist(x_data,y_data,var_names,ranges,colorbar=True,
    #                 saveplot=False,pics_dir=output_dir,plot_title=lund_q2_xb_title.replace("/",""))



    
