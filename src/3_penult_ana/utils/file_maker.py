import pandas as pd
import json
import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os, subprocess
import math
import shutil
from icecream import ic

def make_dir(file_path):

    if os.path.isdir(file_path):
        print('removing previous save directory')
        ## Try to remove tree; if failed show an error using try...except on screen
        try:
            shutil.rmtree(file_path)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
            #shutil.rmtree(save_folder)
        subprocess.call(['mkdir','-p',file_path])
        print(file_path+" now exists")
    else:
        print(file_path+" is not present, creating now")
        subprocess.call(['mkdir','-p',file_path])





