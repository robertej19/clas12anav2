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


g1 = pd.read_pickle("Gen_phi_binned_1.pkl")
g2 = pd.read_pickle("Gen_phi_binned_2.pkl")
g3 = pd.read_pickle("Gen_phi_binned_3.pkl")
g4 = pd.read_pickle("Gen_phi_binned_4.pkl")
g5 = pd.read_pickle("Gen_phi_binned_5.pkl")
g6 = pd.read_pickle("Gen_phi_binned_6.pkl")
g7 = pd.read_pickle("Gen_phi_binned_7.pkl")
g8 = pd.read_pickle("Gen_phi_binned_8.pkl")
g9 = pd.read_pickle("Gen_phi_binned_9.pkl")

g1.loc[:, "gen_counts"] = g1.loc[:, "recon_counts"] + g2.loc[:, "recon_counts"] + g3.loc[:, "recon_counts"]+ \
                        g4.loc[:, "recon_counts"]+ g5.loc[:, "recon_counts"] + g6.loc[:, "recon_counts"] + \
                        g7.loc[:, "recon_counts"] + g8.loc[:, "recon_counts"]+ g9.loc[:, "recon_counts"]

g2 = g1

g2.drop('recon_counts',axis=1,inplace=True)

ic(g2)

g2.to_pickle("all_gen_binned.pkl")
