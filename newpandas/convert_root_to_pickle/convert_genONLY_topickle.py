#!/usr/bin/env python3
"""
A simple script to save Z and X of 6862 nflow project.
"""

import uproot
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
from copy import copy

M = 0.938272081 # target mass
me = 0.5109989461 * 0.001 # electron mass
ebeam = 10.604 # beam energy
pbeam = np.sqrt(ebeam * ebeam - me * me) # beam electron momentum
beam = [0, 0, pbeam] # beam vector
target = [0, 0, 0] # target vector

def dot(vec1, vec2):
    # dot product of two 3d vectors
    return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]

def mag(vec1):
    # L2 norm of vector
    return np.sqrt(dot(vec1, vec1))

def mag2(vec1):
    # square of L2 norm
    return  dot(vec1, vec1)

def cosTheta(vec1, vec2):
    # cosine angle between two 3d vectors
    return dot(vec1,vec2)/np.sqrt(mag2(vec1) * mag2(vec2))

def angle(vec1, vec2):
    # angle between two 3d vectors
    return 180/np.pi*np.arccos(np.minimum(1, cosTheta(vec1, vec2)))

def cross(vec1, vec2):
    # cross product of two 3d vectors
    return [vec1[1]*vec2[2]-vec1[2]*vec2[1], vec1[2]*vec2[0]-vec1[0]*vec2[2], vec1[0]*vec2[1]-vec1[1]*vec2[0]]

def vecAdd(gam1, gam2):
    # add two 3d vectors
    return [gam1[0]+gam2[0], gam1[1]+gam2[1], gam1[2]+gam2[2]]

def pi0Energy(gam1, gam2):
    # reconstructed pi0 energy of two 3d photon momenta
    return mag(gam1)+mag(gam2)

def pi0InvMass(gam1, gam2):
    # pi0 invariant mass of two 3d photon momenta
    pi0mass2 = pi0Energy(gam1, gam2)**2-mag2(vecAdd(gam1, gam2))
    pi0mass2 = np.where(pi0mass2 >= 0, pi0mass2, 10**6)
    pi0mass = np.sqrt(pi0mass2)
    pi0mass = np.where(pi0mass > 100, -1000, pi0mass)
    return pi0mass

def getPhi(vec1):
    # azimuthal angle of one 3d vector
    return 180/np.pi*np.arctan2(vec1[1], vec1[0])

def getTheta(vec1):
    # polar angle of one 3d vector
    return 180/np.pi*np.arctan2(np.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1]), vec1[2])

def getEnergy(vec1, mass):
    # for taken 3d momenta p and mass m, return energy = sqrt(p**2 + m**2)
    return np.sqrt(mag2(vec1)+mass**2)

def readFile(fname):
    #read root using uproot
    ffile = uproot.open(fname)
    tree = ffile["T"]
    return tree

def readEPGG(tree, entry_stop = None):
    
    # data frames and their keys to read Z part
    df_electronGen = pd.DataFrame()
    df_protonGen = pd.DataFrame()
    df_gammaGen = pd.DataFrame()
    eleKeysGen = ["GenEpx", "GenEpy", "GenEpz"]
    proKeysGen = ["GenPpx", "GenPpy", "GenPpz"]
    gamKeysGen = ["GenGpx", "GenGpy", "GenGpz"]
    # read keys
    for key in eleKeysGen:
        df_electronGen[key] = tree[key].array(library="pd", entry_stop=entry_stop)
    for key in proKeysGen:
        df_protonGen[key] = tree[key].array(library="pd", entry_stop=entry_stop)
    for key in gamKeysGen:
        df_gammaGen[key] = tree[key].array(library="pd", entry_stop=entry_stop)

    #convert data type to standard double
    df_electronGen = df_electronGen.astype({"GenEpx": float, "GenEpy": float, "GenEpz": float})
    df_protonGen = df_protonGen.astype({"GenPpx": float, "GenPpy": float, "GenPpz": float})
    df_gammaGen = df_gammaGen.astype({"GenGpx": float, "GenGpy": float, "GenGpz": float})

    #set up a dummy index for merging
    df_electronGen.loc[:,'event'] = df_electronGen.index
    df_protonGen.loc[:,'event'] = df_protonGen.index
    df_gammaGen.loc[:,'event'] = df_gammaGen.index.get_level_values('entry')

    #sort columns for readability
    df_electronGen = df_electronGen.loc[:, ["event", "GenEpx", "GenEpy", "GenEpz"]]

    #two g's to one gg.
    gamGen = [df_gammaGen["GenGpx"], df_gammaGen["GenGpy"], df_gammaGen["GenGpz"]]
    df_gammaGen.loc[:, 'GenGp'] = mag(gamGen)

    gam1 = df_gammaGen[df_gammaGen.index.get_level_values('subentry')==0]
    gam1 = gam1.reset_index(drop=True)
    gam2 = df_gammaGen[df_gammaGen.index.get_level_values('subentry')==1]
    gam2 = gam2.reset_index(drop=True)

    gam1.loc[:,"GenGp2"] = gam2.loc[:,"GenGp"]
    gam1.loc[:,"GenGpx2"] = gam2.loc[:,"GenGpx"]
    gam1.loc[:,"GenGpy2"] = gam2.loc[:,"GenGpy"]
    gam1.loc[:,"GenGpz2"] = gam2.loc[:,"GenGpz"]
    df_gammaGen = gam1

    #sort GenG indices so that GenGp > GenGp2. This is because Gp > Gp2 at reconstruction level.
    df_gammaGencopy = copy(df_gammaGen)
    df_gammaGencopy.loc[:, "GenGp"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGp"], df_gammaGen.loc[:, "GenGp2"])
    df_gammaGencopy.loc[:, "GenGpx"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGpx"], df_gammaGen.loc[:, "GenGpx2"])
    df_gammaGencopy.loc[:, "GenGpy"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGpy"], df_gammaGen.loc[:, "GenGpy2"])
    df_gammaGencopy.loc[:, "GenGpz"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGpz"], df_gammaGen.loc[:, "GenGpz2"])
    df_gammaGencopy.loc[:, "GenGp2"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGp2"], df_gammaGen.loc[:, "GenGp"])
    df_gammaGencopy.loc[:, "GenGpx2"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGpx2"], df_gammaGen.loc[:, "GenGpx"])
    df_gammaGencopy.loc[:, "GenGpy2"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGpy2"], df_gammaGen.loc[:, "GenGpy"])
    df_gammaGencopy.loc[:, "GenGpz2"] = np.where(df_gammaGen["GenGp"]>df_gammaGen["GenGp2"], df_gammaGen.loc[:, "GenGpz2"], df_gammaGen.loc[:, "GenGpz"])
    df_gammaGen = df_gammaGencopy


    #spherical coordinates
    eleGen = [df_electronGen["GenEpx"], df_electronGen["GenEpy"], df_electronGen["GenEpz"]]
    df_electronGen.loc[:, 'GenEp'] = mag(eleGen)
    df_electronGen.loc[:, 'GenEtheta'] = getTheta(eleGen)
    df_electronGen.loc[:, 'GenEphi'] = getPhi(eleGen)

    proGen = [df_protonGen["GenPpx"], df_protonGen["GenPpy"], df_protonGen["GenPpz"]]
    df_protonGen.loc[:, 'GenPp'] = mag(proGen)
    df_protonGen.loc[:, 'GenPtheta'] = getTheta(proGen)
    df_protonGen.loc[:, 'GenPphi'] = getPhi(proGen)

    gamGen = [df_gammaGen["GenGpx"], df_gammaGen["GenGpy"], df_gammaGen["GenGpz"]]
    # df_gammaGen.loc[:, 'GenGp'] = mag(gamGen)
    df_gammaGen.loc[:, 'GenGtheta'] = getTheta(gamGen)
    df_gammaGen.loc[:, 'GenGphi'] = getPhi(gamGen)

    gamGen2 = [df_gammaGen["GenGpx2"], df_gammaGen["GenGpy2"], df_gammaGen["GenGpz2"]]
    debug = df_gammaGen.loc[:, 'GenGp2'] == mag(gamGen2)
    df_gammaGen.loc[:, 'GenGtheta2'] = getTheta(gamGen2)
    df_gammaGen.loc[:, 'GenGphi2'] = getPhi(gamGen2)

    df_z = pd.merge(df_electronGen, df_protonGen, how='inner', on='event')
    df_z = pd.merge(df_z, df_gammaGen, how='inner', on='event')


    return df_z



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f","--fname", help="a single root file to convert into pickles", default="infile.root")
    parser.add_argument("-o","--out", help="a single pickle file name as an output", default="outfile.pkl")
    parser.add_argument("-s","--entry_stop", help="entry_stop to stop reading the root file", default = None)
    
    args = parser.parse_args()

    tree = readFile(args.fname)
    df_gen = readEPGG(tree)


    df_gen.to_pickle("df_genONLY.pkl")

