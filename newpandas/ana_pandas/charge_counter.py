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
    df_after_cuts = pd.read_pickle("real/F18_All_DVPi0_Events.pkl")
    #ic(df_real)

    #make plots after cuts are applied
    ic(df_after_cuts.head(5))

    
    #hist = df_after_cuts.hist(bins=30)
    #plt.show()
    ic(df_after_cuts.columns.values)
    a = df_after_cuts.RunNum.unique()
    
    q_mins = []
    q_maxs = []
    run_nums = []
    
    for run_num_val in a:
        q = "RunNum == {}".format(run_num_val)
        small = df_after_cuts.query(q).beamQ
        q_mins.append(small.min())
        q_maxs.append(small.max())
        run_nums.append(run_num_val)
    
    d = {'RunNum': run_nums, 'beamQ_min': q_mins,'beamQ_max': q_maxs }
    df = pd.DataFrame(data=d)
    df['beamQ_accum'] = df['beamQ_max']-df['beamQ_min']
    total = df.beamQ_accum.sum()
    ic(df)
    ic(total)
    df.to_csv(r'beamq.txt')
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