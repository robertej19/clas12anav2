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

#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker


data_dir = "data/5_pickled_pandas/lund_pickles/"
data_list = os.listdir(data_dir)
ic.disable()

def calculate_kinematics(event_df):
    ic.enable()
    ele = event_df.query("particleID == 11")
    pro = event_df.query("particleID == 2212")
    ic(ele)
    ic(pro)
    photons = event_df.query("particleID == 22")
    ic(photons)


    Eprime = float(ele["E_GeV"].values[0])

    q2 = 0
    xb = 0
    t = 0
    phi = 0
    
    return q2,xb,t,phi,Eprime

def process_lunds_into_events(df):
    events_list = []
    num_events = df["event_num"].max()
    ic(num_events)
    for ind in range(0,2):#num_events):
        if ind % 1000 ==0:
            ic.enable()
            ic(ind)
            ic.disable()
        event_dataframe = df.query("event_num == {}".format(ind))
        
        run_num = 0
        event_num = ind
        lumi = 0
        heli = 0
        Ebeam = 10.6
        
        q2,xb,t,phi,Eprime = calculate_kinematics(event_dataframe)

        events_list.append([run_num,event_num,lumi,heli,
            Ebeam,Eprime,q2,xb,t,phi])
    
    return events_list



out_labels = ["run","event","luminosity","helicity","Ebeam","Eprime","q2","xb","t","phi"]


for lund_pickle in data_list:
    ic(lund_pickle)
    df = data_getter.get_dataframe("lund_pickles/"+lund_pickle)
    events_list = process_lunds_into_events(df)
    df_out = pd.DataFrame(events_list, columns=out_labels)
    ic(df_out)
    print(df_out)
    df_out.to_pickle("lund_processed_pickles/"+lund_pickle)
    