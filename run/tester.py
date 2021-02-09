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
from picture_tools import prelimplot

dirname = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/dvep/output/t_dependence_hists/F18_Inbending_FD_SangbaekSkim_0_20210205/"

prelimplot.stitch_pics(dirname,save_dir="./")