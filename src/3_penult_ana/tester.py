from matplotlib.colors import LinearSegmentedColormap
import numpy as np
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
from utils import data_getter



pickled_df_file = "F18In_168_20210129/skims-168.pkl"
fs = data_getter.get_json_fs()
df = data_getter.get_dataframe(pickled_df_file)


ic(comp_str)

dfq = comp_str
d2 = df.query(dfq)
print(d2)