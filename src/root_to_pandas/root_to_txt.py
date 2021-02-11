#!/usr/bin/python

import uproot
from icecream import ic
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import subprocess
import os
import time
import shutil
from shutil import copyfile


#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker


"""
tree.keys()
['nmb', 'Pp', 'Ppx', 'Ppy', 'Ppz', 'Ptheta', 'Pphi', 
'Pvx', 'Pvy', 'Pvz', 'Pvt', 'PSector', 'Pbeta', 'Pstat', 
'nml', 'Ep', 'Epx', 'Epy', 'Epz', 'Etheta', 'Ephi', 'Evx', 
'Evy', 'Evz', 'Evt', 'Ebeta', 'Estat', 'ESector', 'nmg', 
'Gp', 'Gpx', 'Gpy', 'Gpz', 'Gtheta', 'Gphi', 'Gvx', 'Gvy', 
'Gvz', 'Gvt', 'GSector', 'Gbeta', 'Gstat', 'beamQ', 
'liveTime', 'startTime', 'RFTime', 'helicity', 
'helicityRaw', 'EventNum', 'RunNum', 'Q2', 'Nu', 'q', 'qx',
'qy', 'qz', 'W2', 'xB', 't', 'combint', 'mPpx', 'mPpy',
'mPpz', 'mPp', 'mmP', 'meP', 'Mpx', 'Mpy', 'Mpz', 'Mp',
'mm', 'me', 'mGpx', 'mGpy', 'mGpz', 'mGp', 'mmG', 'meG',
'Pi0p', 'Pi0px', 'Pi0py', 'Pi0pz', 'Pi0theta',
'Pi0phi', 'Pi0M', 'Pi0Sector', 'pIndex', 'gIndex1',
'gIndex2', 'trento', 'trento2', 'trento3']  

"""



fs = data_getter.get_json_fs()


datafile_dir = "testsim_results/"
data_out_dir = "testsim_results/"
#FD
#datafile_dir = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
#data_out_dir = "F18_Inbending_FD_SangbaekSkim_0_20210205/"
#CD
#datafile_dir = "F18_Inbending_CD_SangbaekSkim_0_20210205/"
#data_out_dir = "F18_Inbending_CD_SangbaekSkim_0_20210205/"

data_dir = fs['base_dir']+fs['data_dir']+fs["data_3_dir"]+datafile_dir
data_list = os.listdir(data_dir)


output_dir = fs['base_dir']+fs['data_dir']+fs["data_4_dir"]+data_out_dir
file_maker.make_dir(output_dir)


total_counts = 0
for count,filename in enumerate(data_list):
    print("on file {} out of {}, named {}".format(count+1,len(data_list),filename))

    output_file_ending = filename.replace(".root",".txt")
    
    file = uproot.open(data_dir+filename)
    
    tree = file["T"]

    

    q2 = tree["Q2"].array()
    xB = tree["xB"].array()
    t_mom = tree["t"].array()
    trent1 = tree["trento"].array()
    event_num = tree["EventNum"].array()
    run_num = tree['RunNum'].array()
    heli = tree["helicity"].array()
    lumi = tree['beamQ'].array()
    #trent2 = tree["trento2"].array()
    #trent3 = tree["trento3"].array()
    #pi0M = tree['Pi0M'].array()


    #filt_pi = []
    #filt_trent = []
    #filtering
    #ic.disable()
    
    output_file = open(output_dir+output_file_ending,"w")
    output_file.write("{},{},{},{},{},{},{},{}\n".format("run",
        "event","luminosity","helicity","q2","xb","t","phi",
        ))
    for count,item in enumerate(q2):
    #for count in range(0,10):
        #For now just take 0th element of e.g. trent, phi, this needs to change
        output_file.write("{},{},{},{},{},{},{},{}\n".format(run_num[count],
        event_num[count],lumi[count],heli[count],q2[count],
        xB[count],t_mom[count][0],trent1[count][0],)
        )

    print("done filtering")


    #arr = np.array(filt_trent)

    print("number of events is: {}".format(len(q2)))
    total_counts += len(q2)

print("Done processing, total number of events is: {}".format(total_counts))
